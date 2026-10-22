"""Upload orchestration service for the lecture processing pipeline."""

import os
import shutil

from fastapi import UploadFile

from core.config import settings
from core.logging import get_logger
from managers.lecture_manager import add_lecture
from progress import update_progress
from services.chunk_service import chunk_text
from services.embedding_service import create_embeddings
from services.extract_audio import extract_audio
from services.faiss_service import create_faiss_index
from services.frame_extractor import extract_frames
from services.merge_service import merge_text
from services.ocr_service import extract_text_from_frames
from services.whisper_service import transcribe_audio
from utils.file_utils import ensure_directory
from utils.responses import success_response
from utils.validators import validate_video_upload

logger = get_logger(__name__)


def process_upload(video: UploadFile, user_id: int) -> dict:
    """Validate, store, and process an uploaded lecture video."""

    validate_video_upload(video)

    logger.info("Upload started: %s", video.filename)
    update_progress("Uploading Video", 10)

    upload_folder = ensure_directory(settings.upload_dir)
    file_path = os.path.join(upload_folder, video.filename)

    video.file.seek(0)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    update_progress("Extracting Audio...", 20)
    logger.info("Audio extraction started: %s", file_path)
    audio_path = extract_audio(file_path)

    update_progress("Transcribing Speech...", 35)
    logger.info("Transcription started: %s", audio_path)
    transcript_path = transcribe_audio(audio_path)

    update_progress("Extracting Video Frames...", 50)
    frames_folder = extract_frames(file_path)

    update_progress("Running OCR on Slides...", 65)
    logger.info("OCR started: %s", frames_folder)
    ocr_file = extract_text_from_frames(frames_folder)

    update_progress("Merging Transcript and OCR...", 75)
    final_notes = merge_text(transcript_path, ocr_file)

    update_progress("Creating Text Chunks...", 82)
    chunks, _chunks_file = chunk_text(final_notes)

    update_progress("Creating Embeddings...", 90)
    logger.info("Embedding generation started")
    embedding_file = create_embeddings(chunks)

    update_progress("Building FAISS Index...", 96)
    logger.info("FAISS indexing started")
    faiss_file = create_faiss_index(embedding_file)

    lecture_id = add_lecture(
        user_id=user_id,
        title=video.filename,
        video_path=file_path,
        transcript_path=transcript_path,
        ocr_path=ocr_file,
        merged_path=final_notes,
        embedding_path=embedding_file,
        faiss_path=faiss_file,
    )

    update_progress("Lecture Ready", 100)
    logger.info("Upload completed: lecture_id=%s", lecture_id)

    return success_response(
        "Lecture processed successfully",
        data={"lecture_id": lecture_id},
        legacy={
            "message": "Lecture processed successfully",
            "lecture_id": lecture_id,
        },
    )
