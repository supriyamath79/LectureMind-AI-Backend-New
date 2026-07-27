import pickle
import ollama


def generate_summary(embedding_file):

    with open(embedding_file, "rb") as f:
        data = pickle.load(f)

    chunks = data["chunks"]

    # Use the entire lecture
    lecture = "\n\n".join(chunks)

    prompt = f"""
You are LectureMind AI.

Create professional study notes from the lecture.

Rules:
- Use ONLY the lecture content.
- Do not add external information.
- Use clear headings.
- Include:
  1. Lecture Topic
  2. Overview
  3. Key Concepts
  4. Real-World Applications
  5. Important Terms
  6. Quick Revision Points
- Use bullet points.
- Use simple English.

Lecture:

{lecture}

Generate the study notes:
"""

    response = ollama.chat(
        model="gemma2:2b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0,
            "num_predict": 512,
            "top_p": 0.9,
            "top_k": 40
        }
    )

    return response["message"]["content"]