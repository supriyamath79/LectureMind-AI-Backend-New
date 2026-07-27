from fastapi import APIRouter, Form

from managers.lecture_manager import get_lecture
from services.keypoints_service import generate_keypoints

router = APIRouter()

@router.post("/keypoints")
def get_key_points(
    lecture_id: int = Form(...)
):
    lecture = get_lecture(lecture_id)

    if lecture is None:
        return {
            "keypoints": "Lecture not found."
        }

    keypoints = generate_keypoints(
        lecture["embedding_path"]
    )

    return {
        "keypoints": keypoints
    }