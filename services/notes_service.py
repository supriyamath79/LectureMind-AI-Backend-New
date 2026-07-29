"""Lecture notes service."""

from managers.lecture_manager import get_lecture_for_user
from services.ai_service import generate_completion, load_lecture_from_embeddings
from utils.responses import error_response, success_response


def generate_notes(lecture_id: int, user_id: int) -> dict:
    """Generate detailed study notes for a lecture."""

    lecture = get_lecture_for_user(lecture_id, user_id)

    if lecture is None:
        return error_response(
            "Lecture not found.",
            legacy={"notes": "Lecture not found."},
        )

    lecture_text = load_lecture_from_embeddings(lecture["embedding_path"])

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

{lecture_text}

Study Notes:
"""

    notes = generate_completion(
        prompt,
        options={
            "temperature": 0,
            "num_predict": 800,
            "top_p": 0.9,
            "top_k": 40,
        },
    )

    return success_response(
        "Notes generated successfully.",
        data={"notes": notes},
        legacy={"notes": notes},
    )
