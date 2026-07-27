from fastapi import APIRouter, Form

from managers.lecture_manager import get_lecture
from services.notes_service import generate_notes

router = APIRouter()

@router.post("/notes")
def generate_lecture_notes(
    lecture_id: int = Form(...)
):
    lecture = get_lecture(lecture_id)

    if lecture is None:
        return {
            "notes": "Lecture not found."
        }

    notes = generate_notes(
        lecture["embedding_path"]
    )

    return {
        "notes": notes
    }