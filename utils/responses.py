"""Helpers for consistent API response payloads."""

from typing import Any


def success_response(
    message: str,
    data: Any = None,
    legacy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return a standard success response while preserving legacy top-level fields."""

    payload = {
        "success": True,
        "message": message,
        "data": data or {},
        "error": None,
    }

    if legacy:
        payload.update(legacy)

    return payload


def error_response(
    message: str,
    error: Any = None,
    legacy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return a standard error response while preserving optional legacy fields."""

    payload = {
        "success": False,
        "message": message,
        "data": {},
        "error": error or message,
    }

    if legacy:
        payload.update(legacy)

    return payload
