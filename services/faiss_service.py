"""FAISS indexing service."""

import os
import pickle

import faiss
import numpy as np

from core.config import settings
from core.logging import get_logger
from utils.file_utils import ensure_directory

logger = get_logger(__name__)


def create_faiss_index(embedding_file):
    """Build and persist a FAISS inner-product index."""

    with open(embedding_file, "rb") as f:
        data = pickle.load(f)

    embeddings = np.array(
        data["embeddings"],
        dtype=np.float32,
    )

    faiss.normalize_L2(embeddings)
    logger.debug("Embeddings shape: %s", embeddings.shape)

    if len(embeddings.shape) != 2:
        raise ValueError(f"Invalid embeddings shape: {embeddings.shape}")

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    output_folder = ensure_directory(os.path.join(settings.output_dir, "faiss"))
    faiss_path = os.path.join(output_folder, "index.faiss")
    faiss.write_index(index, faiss_path)

    logger.info("FAISS indexing completed: %s", faiss_path)
    return faiss_path
