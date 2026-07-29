"""Input validation helpers."""

from fastapi import UploadFile

from core.config import settings
from core.exceptions import AppException
from utils.file_utils import get_extension, get_file_size


def validate_video_upload(video: UploadFile | None) -> None:
    """Validate video upload presence, extension, size, and non-empty content."""

    if video is None or not video.filename:
        raise AppException("Video file is required.", status_code=400)

    extension = get_extension(video.filename)
    if extension not in settings.allowed_extensions:
        raise AppException(
            "Unsupported video format.",
            status_code=415,
            error=f"Allowed extensions: {', '.join(settings.allowed_extensions)}",
        )

    size = get_file_size(video.file)
    if size == 0:
        raise AppException("Uploaded video is empty.", status_code=400)

    if size > settings.max_upload_size_bytes:
        raise AppException("Uploaded video is too large.", status_code=413)
