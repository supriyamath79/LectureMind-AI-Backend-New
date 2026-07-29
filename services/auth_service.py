"""Authentication and user profile service."""

import re
from sqlite3 import IntegrityError

from core.config import settings
from core.exceptions import AppException
from core.security import create_token, hash_password, verify_password
from managers.user_manager import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    update_last_login,
)
from utils.responses import success_response

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def public_user(user) -> dict:
    """Return the public user profile shape."""

    return {
        "id": user["id"],
        "full_name": user["full_name"],
        "email": user["email"],
        "created_at": user["created_at"],
        "last_login": user["last_login"],
    }


def validate_password(password: str, confirm_password: str | None = None) -> None:
    """Validate password strength and optional confirmation."""

    if confirm_password is not None and password != confirm_password:
        raise AppException("Passwords do not match.", status_code=400)

    if len(password) < 8:
        raise AppException("Password must be at least 8 characters.", status_code=400)

    if not re.search(r"[A-Z]", password):
        raise AppException("Password must contain an uppercase letter.", status_code=400)

    if not re.search(r"[a-z]", password):
        raise AppException("Password must contain a lowercase letter.", status_code=400)

    if not re.search(r"\d", password):
        raise AppException("Password must contain a number.", status_code=400)


def register_user(full_name: str, email: str, password: str, confirm_password: str) -> dict:
    """Register a new user with a bcrypt password hash."""

    full_name = full_name.strip()
    email = email.strip().lower()

    if len(full_name) < 2:
        raise AppException("Full name is required.", status_code=400)

    if not EMAIL_PATTERN.match(email):
        raise AppException("A valid email is required.", status_code=400)

    validate_password(password, confirm_password)

    if get_user_by_email(email):
        raise AppException("Email is already registered.", status_code=409)

    try:
        user_id = create_user(full_name, email, hash_password(password))
    except IntegrityError as exc:
        raise AppException("Email is already registered.", status_code=409) from exc

    user = get_user_by_id(user_id)
    return success_response(
        "Registration successful.",
        data={"user": public_user(user)},
        legacy={"user": public_user(user)},
    )


def login_user(email: str, password: str, remember_me: bool = False) -> dict:
    """Authenticate a user and return JWT tokens."""

    user = get_user_by_email(email.strip().lower())

    if user is None or not verify_password(password, user["password_hash"]):
        raise AppException("Invalid email or password.", status_code=401)

    update_last_login(user["id"])
    user = get_user_by_id(user["id"])

    access_expiry = (
        settings.remember_me_access_token_expire_minutes
        if remember_me
        else settings.access_token_expire_minutes
    )
    access_token = create_token(user["id"], access_expiry, "access")
    refresh_token = create_token(user["id"], settings.refresh_token_expire_minutes, "refresh")

    data = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": public_user(user),
    }
    return success_response(
        "Login successful.",
        data=data,
        legacy=data,
    )


def get_profile(user_id: int) -> dict:
    """Return the authenticated user's profile."""

    user = get_user_by_id(user_id)

    if user is None:
        raise AppException("User not found.", status_code=404)

    profile = public_user(user)
    return success_response(
        "Profile fetched successfully.",
        data={"user": profile},
        legacy={"user": profile},
    )
