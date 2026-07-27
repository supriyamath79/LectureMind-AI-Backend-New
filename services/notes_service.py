import pickle
import ollama

def generate_notes(embedding_file):
    with open(embedding_file, "rb") as f:
        data = pickle.load(f)

    chunks = data["chunks"]
    lecture = "\n\n".join(chunks)

    prompt = f"""
You are LectureMind AI.

Create detailed study notes from the lecture.

Rules:
- Use ONLY the lecture content.
- Do not add outside knowledge.
- Use simple English.
- Organize into sections with headings.
- Use bullet points.
- Include examples only if mentioned in the lecture.

Lecture:

{lecture}

Study Notes:
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
            "num_predict": 800,
            "top_p": 0.9,
            "top_k": 40,
        },
    )

    return response["message"]["content"]