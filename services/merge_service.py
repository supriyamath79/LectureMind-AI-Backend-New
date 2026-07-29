"""Transcript and OCR merge service."""

import os
import re

from core.config import settings
from utils.file_utils import ensure_directory


def merge_text(transcript_file, ocr_file):
    """Merge Whisper transcript and cleaned OCR text into final notes."""

    output_folder = ensure_directory(os.path.join(settings.output_dir, "final_notes"))
    output_file = os.path.join(output_folder, "final_notes.txt")

    with open(transcript_file, "r", encoding="utf-8") as t:
        transcript = t.read()

    with open(ocr_file, "r", encoding="utf-8") as o:
        ocr_lines = o.readlines()

    cleaned_ocr = []

    for line in ocr_lines:
        line = line.strip()

        if not line:
            continue
        if "frame_" in line:
            continue
        if "====" in line:
            continue
        if len(line) < 15:
            continue

        letters = re.findall(r"[A-Za-z]", line)
        if len(letters) < 8:
            continue

        cleaned_ocr.append(line)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("========== TRANSCRIPT ==========\n\n")
        f.write(transcript)
        f.write("\n\n========== IMPORTANT TEXT FROM SLIDES ==========\n\n")

        for line in cleaned_ocr:
            f.write(line + "\n")

    return output_file
