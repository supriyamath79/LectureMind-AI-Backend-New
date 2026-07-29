"""Quiz API routes."""

from fastapi import APIRouter, Depends, Form

from dependencies.auth import get_current_user
from services.quiz_service import generate_quiz

router = APIRouter()


@router.post("/quiz")
def generate_lecture_quiz(lecture_id: int = Form(...), current_user=Depends(get_current_user)):
    """Generate a lecture quiz."""

    return generate_quiz(lecture_id, current_user["id"])
