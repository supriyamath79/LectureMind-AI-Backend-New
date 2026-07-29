"""Question answering API routes."""

from fastapi import APIRouter, Depends, Form

from dependencies.auth import get_current_user
from services.llm_service import answer_question

router = APIRouter()


@router.post("/ask")
def ask_question(
    lecture_id: int = Form(...),
    question: str = Form(...),
    current_user=Depends(get_current_user),
):
    """Answer a question using lecture context."""

    return answer_question(lecture_id, question, current_user["id"])
