from fastapi import APIRouter, Form

from managers.lecture_manager import get_lecture
from services.quiz_service import generate_quiz

router = APIRouter()


@router.post("/quiz")
def generate_lecture_quiz(
    lecture_id: int = Form(...)
):
    lecture = get_lecture(lecture_id)

    if lecture is None:
        return {
            "quiz": []
        }

    quiz = generate_quiz(
        lecture["embedding_path"]
    )

    return {
        "quiz": quiz
    }