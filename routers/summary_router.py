from fastapi import APIRouter, Form

from managers.lecture_manager import get_lecture
from services.summary_service import generate_summary

router = APIRouter()


@router.post("/summary")
def summarize_lecture(
    lecture_id: int = Form(...)
):
    lecture = get_lecture(lecture_id)

    if lecture is None:
        return {
            "summary": "Lecture not found."
        }

    summary = generate_summary(
        lecture["embedding_path"]
    )

    return {
        "summary": summary
    }