"""FAISS retrieval service."""

import pickle

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from core.config import settings
from core.logging import get_logger

logger = get_logger(__name__)

model = SentenceTransformer(settings.embedding_model)


def retrieve_chunks(question, embedding_file, faiss_file):
    """Retrieve relevant chunks for a question from a FAISS index."""

    with open(embedding_file, "rb") as f:
        data = pickle.load(f)

    chunks = data["chunks"]
    index = faiss.read_index(faiss_file)

    question_embedding = model.encode(
        [question],
        normalize_embeddings=True,
    )
    question_embedding = np.array(
        question_embedding,
        dtype=np.float32,
    )

    faiss.normalize_L2(question_embedding)

    distances, indices = index.search(
        question_embedding,
        k=6,
    )

    results = []
    seen = set()

    logger.debug("Similarity scores: %s", distances[0])

    for score, idx in zip(distances[0], indices[0]):
        if idx == -1:
            continue

        if score < settings.retrieval_similarity_threshold:
            continue

        chunk = chunks[idx]

        if chunk in seen:
            continue

        seen.add(chunk)
        results.append(chunk)
        

    best_score = float(distances[0][0])
    logger.info("Retrieved %s chunks with best score %.4f", len(results), best_score)

    return {
        "chunks": results,
        "best_score": best_score,
    }
