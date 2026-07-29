"""OCR service for extracted lecture frames."""

import os
import shutil

import cv2
import easyocr

from core.config import settings
from core.logging import get_logger
from progress import update_progress
from utils.file_utils import ensure_directory

logger = get_logger(__name__)

reader = easyocr.Reader(["en"])


def extract_text_from_frames(frame_folder):
    """Extract slide text from frame images and persist it to a text file."""

    output_folder = os.path.join(settings.output_dir, "ocr")

    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)

    ensure_directory(output_folder)
    output_file = os.path.join(output_folder, "slides_text.txt")

    with open(output_file, "w", encoding="utf-8") as f:
        images = sorted(os.listdir(frame_folder))
        jpg_images = [image for image in images if image.endswith(".jpg")]
        total_images = len(jpg_images)
        processed = 0

        for image in jpg_images:
            logger.debug("OCR processing frame: %s", image)
            processed += 1

            if total_images:
                progress = 65 + int((processed / total_images) * 25)
                update_progress(
                    f"Reading Slides ({processed}/{total_images})",
                    progress,
                )

            image_path = os.path.join(frame_folder, image)
            img = cv2.imread(image_path)
            img = cv2.resize(
                img,
                None,
                fx=0.6,
                fy=0.6,
                interpolation=cv2.INTER_AREA,
            )
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (3, 3), 0)
            processed_image = cv2.adaptiveThreshold(
                gray,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                11,
                2,
            )

            result = reader.readtext(processed_image, detail=0)
            text = " ".join(result)

            f.write(f"\n===== {image} =====\n")
            f.write(text)
            f.write("\n\n")

    logger.info("OCR completed: %s", output_file)
    return output_file
