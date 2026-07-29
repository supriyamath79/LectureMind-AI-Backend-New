"""Summary API routes."""

from fastapi import APIRouter, Depends, Form

from dependencies.auth import get_current_user
from services.summary_service import generate_summary

router = APIRouter()


@router.post("/summary")
def summarize_lecture(lecture_id: int = Form(...), current_user=Depends(get_current_user)):
    """Generate a lecture summary."""

    return generate_summary(lecture_id, current_user["id"])
