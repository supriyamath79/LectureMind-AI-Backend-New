"""Sentence embedding service."""

import os
import pickle

from sentence_transformers import SentenceTransformer

from core.config import settings
from core.logging import get_logger
from utils.file_utils import ensure_directory

logger = get_logger(__name__)

model = SentenceTransformer(settings.embedding_model)


def create_embeddings(chunks):
    """Create normalized sentence embeddings and persist them."""

    embeddings = model.encode(
        chunks,
        normalize_embeddings=True,
        convert_to_numpy=True,
    )

    output_folder = ensure_directory(os.path.join(settings.output_dir, "embeddings"))
    output_file = os.path.join(output_folder, "embeddings.pkl")

    with open(output_file, "wb") as f:
        pickle.dump(
            {
                "chunks": chunks,
                "embeddings": embeddings,
            },
            f,
        )

    logger.info("Embedding generation completed: %s", output_file)
    return output_file
