import pickle
import ollama

def generate_keypoints(embedding_file):
    with open(embedding_file, "rb") as f:
        data = pickle.load(f)

    chunks = data["chunks"]
    lecture = "\n\n".join(chunks)

    prompt = f"""
You are LectureMind AI.

Extract ONLY the most important key points from the lecture.

Rules:
- Use ONLY the lecture content.
- Do NOT add outside knowledge.
- Return 10-15 concise bullet points.
- Each point should be one sentence.
- Do not repeat information.

Lecture:

{lecture}

Key Points:
"""

    response = ollama.chat(
        model="gemma2:2b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        options={
            "temperature": 0,
            "num_predict": 400,
            "top_p": 0.9,
            "top_k": 40,
        },
    )

    return response["message"]["content"]