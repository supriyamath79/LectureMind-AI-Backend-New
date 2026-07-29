"""Upload API routes."""

from fastapi import APIRouter, Depends, File, UploadFile

from dependencies.auth import get_current_user
from services.upload_service import process_upload

router = APIRouter()


@router.post("/upload")
def upload_video(video: UploadFile = File(...), current_user=Depends(get_current_user)):
    """Upload and process a lecture video."""

    return process_upload(video, current_user["id"])
