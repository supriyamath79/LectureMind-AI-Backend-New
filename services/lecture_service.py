"""Lecture application service."""

from managers.lecture_manager import delete_lecture, get_all_lectures, get_lecture_for_user
from utils.responses import error_response, success_response


def list_lecture_records(user_id: int) -> dict:
    """Return all lectures in the existing API shape plus standard response metadata."""

    lectures = [dict(lecture) for lecture in get_all_lectures(user_id)]
    return success_response(
        "Lectures fetched successfully.",
        data={"lectures": lectures},
        legacy={"lectures": lectures},
    )


def get_lecture_details(lecture_id: int, user_id: int):
    """Return lecture details or a compatible not-found response."""

    lecture = get_lecture_for_user(lecture_id, user_id)
    if lecture is None:
        return error_response(
            "Lecture not found.",
            legacy={"message": "Lecture not found."},
        )

    lecture_data = dict(lecture)
    return success_response(
        "Lecture fetched successfully.",
        data=lecture_data,
        legacy=lecture_data,
    )


def remove_lecture_record(lecture_id: int, user_id: int) -> dict:
    """Delete a lecture record using the existing manager behavior."""

    lecture = get_lecture_for_user(lecture_id, user_id)
    if lecture is None:
        return error_response(
            "Lecture not found.",
            legacy={"message": "Lecture not found."},
        )

    delete_lecture(lecture_id, user_id)
    return success_response(
        "Lecture deleted successfully.",
        legacy={"message": "Lecture deleted successfully."},
    )
