"""Reusable file and path helpers."""

import os
import shutil
from pathlib import Path


def ensure_directory(path: str) -> str:
    """Create a directory if it does not already exist and return the path."""

    os.makedirs(path, exist_ok=True)
    return path


def get_extension(filename: str | None) -> str:
    """Return the lowercase file extension for a filename."""

    return Path(filename or "").suffix.lower()


def get_file_size(file_object) -> int:
    """Return upload size without changing the caller-visible stream position."""

    current_position = file_object.tell()
    file_object.seek(0, os.SEEK_END)
    size = file_object.tell()
    file_object.seek(current_position)
    return size


def remove_path(path: str | None) -> None:
    """Remove a file or directory if it exists."""

    if not path or not os.path.exists(path):
        return

    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)
