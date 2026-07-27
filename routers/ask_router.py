from fastapi import APIRouter, Form

from managers.lecture_manager import get_lecture
from services.retrieve_service import retrieve_chunks
from services.llm_service import generate_answer

router = APIRouter()


@router.post("/ask")
def ask_question(
    lecture_id: int = Form(...),
    question: str = Form(...)
):
    lecture = get_lecture(lecture_id)

    if lecture is None:
        return {
            "message": "Lecture not found."
        }

    embedding_file = lecture["embedding_path"]
    faiss_file = lecture["faiss_path"]

    retrieved = retrieve_chunks(
        question,
        embedding_file,
        faiss_file
    )

    chunks = retrieved["chunks"]
    best_score = retrieved["best_score"]

    print("\n===================================")
    print("BEST SIMILARITY SCORE:", best_score)
    print("===================================\n")

    if best_score < 0.40:
        return {
            "answer": "I could not find the answer in the lecture."
        }

    answer = generate_answer(
        question,
        chunks
    )

    return {
        "answer": answer
    }