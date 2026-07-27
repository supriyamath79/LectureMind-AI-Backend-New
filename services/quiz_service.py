import pickle
import json
import ollama
from sympy import content


def generate_quiz(embedding_file):
    with open(embedding_file, "rb") as f:
        data = pickle.load(f)

    chunks = data["chunks"]
    lecture = "\n\n".join(chunks)

    prompt = f"""
You are LectureMind AI.

Generate exactly 5 multiple-choice questions based ONLY on the lecture.

Rules:
- Return ONLY valid JSON.
- Do NOT include markdown.
- Do NOT include explanations outside JSON.
- Do NOT add text before or after JSON.
- Each question must have:
  - question
  - options (exactly 4)
  - answer
  - explanation

Required format:

[
  {{
    "question": "Question text",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "answer": "Correct Option",
    "explanation": "Short explanation"
  }}
]

Lecture:

{lecture}
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
            "num_predict": 700,
            "top_p": 0.9,
            "top_k": 40,
        },
    )

    content = response["message"]["content"]

    print("\n================ AI RESPONSE ================\n")
    print(content)
    print("\n=============================================\n")

    try:
        quiz = json.loads(content)
    except Exception as e:
        print("JSON Error:", e)
        quiz = []

    return quiz