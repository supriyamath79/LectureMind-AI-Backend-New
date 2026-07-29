"""Video frame extraction service."""

import os
import shutil

import cv2

from core.config import settings
from core.logging import get_logger
from utils.file_utils import ensure_directory

logger = get_logger(__name__)


def extract_frames(video_path):
    """Extract one frame every five seconds from a lecture video."""

    output_folder = os.path.join(settings.output_dir, "frames")

    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)

    ensure_directory(output_folder)

    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_interval = max(1, int(fps * 5))

    count = 0
    saved = 0

    while True:
        success, frame = video.read()

        if not success:
            break

        if count % frame_interval == 0:
            frame_path = os.path.join(output_folder, f"frame_{saved}.jpg")
            cv2.imwrite(frame_path, frame)
            saved += 1

        count += 1

    video.release()
    logger.info("Frame extraction completed: %s frames", saved)

    return output_folder
