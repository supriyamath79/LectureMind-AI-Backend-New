"""Lecture text chunking service."""

import os

from langchain_text_splitters import RecursiveCharacterTextSplitter

from core.config import settings
from utils.file_utils import ensure_directory


def chunk_text(final_notes_path):
    """Split final lecture notes into retrieval chunks."""

    with open(final_notes_path, "r", encoding="utf-8") as f:
        text = f.read()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = splitter.split_text(text)

    output_folder = ensure_directory(os.path.join(settings.output_dir, "chunks"))
    output_file = os.path.join(output_folder, "chunks.txt")

    with open(output_file, "w", encoding="utf-8") as f:
        for i, chunk in enumerate(chunks):
            f.write(f"========== Chunk {i+1} ==========\n\n")
            f.write(chunk)
            f.write("\n\n")

    return chunks, output_file
