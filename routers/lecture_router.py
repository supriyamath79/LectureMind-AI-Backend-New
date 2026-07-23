from fastapi import APIRouter

from managers.lecture_manager import (
    get_all_lectures,
    get_lecture,
    delete_lecture
)

router = APIRouter()


@router.get("/lectures")
def list_lectures():
    lectures = get_all_lectures()

    return {
        "lectures": lectures
    }


@router.get("/lecture/{lecture_id}")
def lecture_details(lecture_id: int):
    lecture = get_lecture(lecture_id)

    if lecture is None:
        return {
            "message": "Lecture not found."
        }

    return lecture


@router.delete("/lecture/{lecture_id}")
def remove_lecture(lecture_id: int):

    delete_lecture(lecture_id)

    return {
        "message": "Lecture deleted successfully."
    }