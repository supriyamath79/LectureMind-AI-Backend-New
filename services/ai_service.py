"""Shared AI completion service."""

import ollama

from core.config import settings
from core.logging import get_logger

logger = get_logger(__name__)


def generate_completion(prompt: str, options: dict) -> str:
    """Generate text from the configured Ollama model."""

    logger.info("AI completion started")
    response = ollama.chat(
        model=settings.ollama_model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        options=options,
    )
    logger.info("AI completion finished")
    return response["message"]["content"]


def load_lecture_from_embeddings(embedding_file: str) -> str:
    """Load lecture chunks from an embeddings pickle file and join them."""

    import pickle

    with open(embedding_file, "rb") as f:
        data = pickle.load(f)

    return "\n\n".join(data["chunks"])
