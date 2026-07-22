from progress import get_progress, update_progress
from services.llm_service import generate_answer
from services.retrieve_service import retrieve_chunks
from services.faiss_service import create_faiss_index
from services.embedding_service import create_embeddings
from services.chunk_service import chunk_text
from services.merge_service import merge_text
from services.ocr_service import extract_text_from_frames
from services.frame_extractor import extract_frames
from services.whisper_service import transcribe_audio
from services.extract_audio import extract_audio
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, Form
import shutil
import os
# Store the latest processed lecture
current_embedding_file = None
current_faiss_file = None
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "Welcome to LectureMind AI Backend"
    }
@app.get("/status")
def status():
    return get_progress()

@app.post("/upload")
def upload_video(
        video: UploadFile = File(...),
    ):
    update_progress("Uploading Video", 10)
    upload_folder = "../uploads"
    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, video.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)
    update_progress("🎤 Extracting Audio...", 20)
    audio_path = extract_audio(file_path)
    update_progress("📝 Transcribing Speech...", 35)
    transcript_path = transcribe_audio(audio_path)
    update_progress("🖼️ Extracting Video Frames...", 50)

    frames_folder = extract_frames(file_path)
    update_progress("🔍 Running OCR on Slides...", 65)
    ocr_file = extract_text_from_frames(frames_folder)
    update_progress("📄 Merging Transcript and OCR...", 75)
    final_notes = merge_text(
    transcript_path,
    ocr_file
    
)
    update_progress("✂️ Creating Text Chunks...", 82)
    chunks, chunks_file = chunk_text(final_notes)
    update_progress("🧠 Creating Embeddings...", 90)
    embedding_file = create_embeddings(chunks)
    update_progress("📚 Building FAISS Index...", 96)
    faiss_file = create_faiss_index(
    embedding_file
)
    update_progress("✅ Lecture Ready", 100)
    global current_embedding_file
    global current_faiss_file

    current_embedding_file = embedding_file
    current_faiss_file = faiss_file
   

    return {
    "message": "Lecture processed successfully"
}
@app.post("/ask")
def ask_question(question: str = Form(...)):

    global current_embedding_file
    global current_faiss_file

    if current_embedding_file is None or current_faiss_file is None:
        return {
            "message": "Please upload a lecture first."
        }

    # Retrieve chunks + similarity score
    retrieved = retrieve_chunks(
        question,
        current_embedding_file,
        current_faiss_file
    )

    chunks = retrieved["chunks"]
    best_score = retrieved["best_score"]

    print("\n===================================")
    print("BEST SIMILARITY SCORE:", best_score)
    print("===================================\n")

    # Reject unrelated questions
    if best_score < 0.60:
        return {
            "answer": "I could not find the answer in the lecture."
        }

    # Generate answer
    answer = generate_answer(
        question,
        chunks
    )

    return {
        "answer": answer
    }