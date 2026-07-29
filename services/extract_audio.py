"""Audio extraction service."""

import os

import ffmpeg

from core.config import settings
from core.logging import get_logger
from utils.file_utils import ensure_directory

logger = get_logger(__name__)


def extract_audio(video_path):
    """Extract mono 16kHz WAV audio from a lecture video."""

    output_folder = ensure_directory(os.path.join(settings.output_dir, "audio"))
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    audio_path = os.path.join(output_folder, f"{video_name}.wav")

    (
        ffmpeg.input(video_path)
        .output(audio_path, acodec="pcm_s16le", ac=1, ar="16000")
        .overwrite_output()
        .run()
    )

    logger.info("Audio extraction completed: %s", audio_path)
    return audio_path
