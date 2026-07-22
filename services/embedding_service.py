from sentence_transformers import SentenceTransformer
import os
import pickle

# Load model only once
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks):

    embeddings = model.encode(
    chunks,
    normalize_embeddings=True,
    convert_to_numpy=True
)

    output_folder = "../outputs/embeddings"
    os.makedirs(output_folder, exist_ok=True)

    output_file = os.path.join(
        output_folder,
        "embeddings.pkl"
    )

    with open(output_file, "wb") as f:
        pickle.dump(
            {
                "chunks": chunks,
                "embeddings": embeddings
            },
            f
        )

    return output_file