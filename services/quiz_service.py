"""Lecture quiz service."""

import json

from core.logging import get_logger
from managers.lecture_manager import get_lecture_for_user
from services.ai_service import generate_completion, load_lecture_from_embeddings
from utils.responses import error_response, success_response

logger = get_logger(__name__)


def generate_quiz(lecture_id: int, user_id: int) -> dict:
    """Generate a five-question multiple-choice quiz for a lecture."""

    lecture = get_lecture_for_user(lecture_id, user_id)

    if lecture is None:
        return error_response(
            "Lecture not found.",
            legacy={"quiz": []},
        )

    lecture_text = load_lecture_from_embeddings(lecture["embedding_path"])

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

{lecture_text}
"""

    content = generate_completion(
        prompt,
        options={
            "temperature": 0,
            "num_predict": 700,
            "top_p": 0.9,
            "top_k": 40,
        },
    )

    try:
        quiz = json.loads(content)
    except Exception as exc:
        logger.warning("Quiz JSON parsing failed: %s", exc)
        quiz = []

    return success_response(
        "Quiz generated successfully.",
        data={"quiz": quiz},
        legacy={"quiz": quiz},
    )
