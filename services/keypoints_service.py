"""Lecture key points service."""

from managers.lecture_manager import get_lecture_for_user
from services.ai_service import generate_completion, load_lecture_from_embeddings
from utils.responses import error_response, success_response


def generate_keypoints(lecture_id: int, user_id: int) -> dict:
    """Generate concise key points for a lecture."""

    lecture = get_lecture_for_user(lecture_id, user_id)

    if lecture is None:
        return error_response(
            "Lecture not found.",
            legacy={"keypoints": "Lecture not found."},
        )

    lecture_text = load_lecture_from_embeddings(lecture["embedding_path"])

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

{lecture_text}

Key Points:
"""

    keypoints = generate_completion(
        prompt,
        options={
            "temperature": 0,
            "num_predict": 400,
            "top_p": 0.9,
            "top_k": 40,
        },
    )

    return success_response(
        "Key points generated successfully.",
        data={"keypoints": keypoints},
        legacy={"keypoints": keypoints},
    )
