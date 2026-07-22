import faiss
import pickle
import os
import numpy as np


def create_faiss_index(embedding_file):

    with open(embedding_file, "rb") as f:
        data = pickle.load(f)

    embeddings = np.array(
    data["embeddings"],
    dtype=np.float32
)

    faiss.normalize_L2(embeddings)
    print("Embeddings Shape:", embeddings.shape)
    if len(embeddings.shape) != 2:
        raise Exception(
            f"Invalid embeddings shape: {embeddings.shape}"
    )


    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    output_folder = "../outputs/faiss"
    os.makedirs(output_folder, exist_ok=True)

    faiss.write_index(
        index,
        os.path.join(output_folder, "index.faiss")
    )

    return os.path.join(
        output_folder,
        "index.faiss"
    )