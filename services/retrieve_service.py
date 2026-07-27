import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_chunks(question, embedding_file, faiss_file):

    with open(embedding_file, "rb") as f:
        data = pickle.load(f)

    chunks = data["chunks"]

    index = faiss.read_index(faiss_file)

    question_embedding = model.encode(
        [question],
        normalize_embeddings=True
    )

    question_embedding = np.array(
        question_embedding,
        dtype=np.float32
    )

    faiss.normalize_L2(question_embedding)

    distances, indices = index.search(
        question_embedding,
        k=6
    )

    results = []
    seen = set()

    SIMILARITY_THRESHOLD = 0.5

    print("==============================")
    print("Similarity Scores")
    print("==============================")

    for score in distances[0]:
        print(score)

    for score, idx in zip(distances[0], indices[0]):

        if idx == -1:
            continue

        if score < SIMILARITY_THRESHOLD:
            continue

        chunk = chunks[idx]

        if chunk in seen:
            continue

        seen.add(chunk)
        results.append(chunk)

    print("\n========== RETRIEVED CHUNKS ==========\n")

    for i, chunk in enumerate(results):
        print(f"\nChunk {i+1}:\n")
        print(chunk)
        print("-" * 60)

    best_score = float(distances[0][0])

    return {
        "chunks": results,
        "best_score": best_score
    }