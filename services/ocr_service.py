import easyocr
import os
import shutil
import cv2
from progress import update_progress

reader = easyocr.Reader(['en'])


def extract_text_from_frames(frame_folder):

    output_folder = "../outputs/ocr"

    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)

    os.makedirs(output_folder, exist_ok=True)

    output_file = os.path.join(output_folder, "slides_text.txt")

    with open(output_file, "w", encoding="utf-8") as f:

        images = sorted(os.listdir(frame_folder))
        total_images = len([img for img in images if img.endswith(".jpg")])
        processed = 0

        for image in images:

            if image.endswith(".jpg"):

                print(f"Processing: {image}")

                processed += 1

                progress = 65 + int((processed / total_images) * 25)

                update_progress(
                    f"🔍 Reading Slides ({processed}/{total_images})",
                    progress
                )

                image_path = os.path.join(frame_folder, image)

                img = cv2.imread(image_path)

                # Resize
                img = cv2.resize(
                    img,
                    None,
                    fx=0.6,
                    fy=0.6,
                    interpolation=cv2.INTER_AREA
                )

                # Convert to grayscale
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # Remove noise
                gray = cv2.GaussianBlur(gray, (3, 3), 0)

                # Improve text visibility
                processed_image = cv2.adaptiveThreshold(
                gray,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                11,
                2
            )

                result = reader.readtext(processed_image, detail=0)

                text = " ".join(result)

                f.write(f"\n===== {image} =====\n")
                f.write(text)
                f.write("\n\n")

    print("OCR Finished")

    return output_file