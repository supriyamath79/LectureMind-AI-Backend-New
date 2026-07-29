"""Whisper transcription service."""

import os

import whisper

from core.config import settings
from core.logging import get_logger
from utils.file_utils import ensure_directory

logger = get_logger(__name__)

model = whisper.load_model(settings.whisper_model)


def transcribe_audio(audio_path):
    """Transcribe an audio file and persist the transcript."""

    logger.info("Transcription started: %s", audio_path)
    result = model.transcribe(audio_path)

    output_folder = ensure_directory(os.path.join(settings.output_dir, "transcripts"))
    transcript_name = os.path.splitext(os.path.basename(audio_path))[0] + ".txt"
    transcript_path = os.path.join(output_folder, transcript_name)

    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(result["text"])

    logger.info("Transcription completed: %s", transcript_path)
    return transcript_path
