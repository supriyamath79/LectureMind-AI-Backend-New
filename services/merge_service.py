import os
import re

def merge_text(transcript_file, ocr_file):

    output_folder = "../outputs/final_notes"
    os.makedirs(output_folder, exist_ok=True)

    output_file = os.path.join(output_folder, "final_notes.txt")

    with open(transcript_file, "r", encoding="utf-8") as t:
        transcript = t.read()

    with open(ocr_file, "r", encoding="utf-8") as o:
        ocr_lines = o.readlines()

    cleaned_ocr = []

    for line in ocr_lines:

        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Skip frame headings
        if "frame_" in line:
            continue

        # Skip separators
        if "====" in line:
            continue

        # Skip very short text
        if len(line) < 15:
            continue

        # Skip lines with very few letters (likely OCR noise)
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