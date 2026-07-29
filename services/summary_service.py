"""Lecture summary service."""

from managers.lecture_manager import get_lecture_for_user
from services.ai_service import generate_completion, load_lecture_from_embeddings
from utils.responses import error_response, success_response


def generate_summary(lecture_id: int, user_id: int) -> dict:
    """Generate professional study notes summary for a lecture."""

    lecture = get_lecture_for_user(lecture_id, user_id)

    if lecture is None:
        return error_response(
            "Lecture not found.",
            legacy={"summary": "Lecture not found."},
        )

    lecture_text = load_lecture_from_embeddings(lecture["embedding_path"])

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

{lecture_text}

Generate the study notes:
"""

    summary = generate_completion(
        prompt,
        options={
            "temperature": 0,
            "num_predict": 512,
            "top_p": 0.9,
            "top_k": 40,
        },
    )

    return success_response(
        "Summary generated successfully.",
        data={"summary": summary},
        legacy={"summary": summary},
    )
