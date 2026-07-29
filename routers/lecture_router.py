"""Lecture API routes."""

from fastapi import APIRouter, Depends

from dependencies.auth import get_current_user
from services.lecture_service import (
    get_lecture_details,
    list_lecture_records,
    remove_lecture_record,
)

router = APIRouter()


@router.get("/lectures")
def list_lectures(current_user=Depends(get_current_user)):
    """List processed lectures."""

    return list_lecture_records(current_user["id"])


@router.get("/lecture/{lecture_id}")
def lecture_details(lecture_id: int, current_user=Depends(get_current_user)):
    """Return details for one lecture."""

    return get_lecture_details(lecture_id, current_user["id"])


@router.delete("/lecture/{lecture_id}")
def remove_lecture(lecture_id: int, current_user=Depends(get_current_user)):
    """Delete one lecture."""

    return remove_lecture_record(lecture_id, current_user["id"])
