from fastapi import APIRouter, UploadFile, File
import os
import shutil

from progress import update_progress
from managers.lecture_manager import add_lecture

from services.extract_audio import extract_audio
from services.whisper_service import transcribe_audio
from services.frame_extractor import extract_frames
from services.ocr_service import extract_text_from_frames
from services.merge_service import merge_text
from services.chunk_service import chunk_text
from services.embedding_service import create_embeddings
from services.faiss_service import create_faiss_index

router = APIRouter()


@router.post("/upload")
def upload_video(video: UploadFile = File(...)):

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
        ocr_file,
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

    lecture_id = add_lecture(
        title=video.filename,
        video_path=file_path,
        transcript_path=transcript_path,
        ocr_path=ocr_file,
        merged_path=final_notes,
        embedding_path=embedding_file,
        faiss_path=faiss_file,
    )

    return {
        "message": "Lecture processed successfully",
        "lecture_id": lecture_id
    }