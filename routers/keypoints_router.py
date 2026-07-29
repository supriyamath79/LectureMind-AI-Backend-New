"""Key points API routes."""

from fastapi import APIRouter, Depends, Form

from dependencies.auth import get_current_user
from services.keypoints_service import generate_keypoints

router = APIRouter()


@router.post("/keypoints")
def get_key_points(lecture_id: int = Form(...), current_user=Depends(get_current_user)):
    """Generate key points for a lecture."""

    return generate_keypoints(lecture_id, current_user["id"])
