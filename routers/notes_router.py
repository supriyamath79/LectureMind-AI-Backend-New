"""Notes API routes."""

from fastapi import APIRouter, Depends, Form

from dependencies.auth import get_current_user
from services.notes_service import generate_notes

router = APIRouter()


@router.post("/notes")
def generate_lecture_notes(lecture_id: int = Form(...), current_user=Depends(get_current_user)):
    """Generate detailed lecture notes."""

    return generate_notes(lecture_id, current_user["id"])
