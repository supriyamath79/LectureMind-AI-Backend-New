"""Password hashing and JWT helpers."""

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from core.config import settings
from core.exceptions import AppException


def hash_password(password: str) -> str:
    """Hash a password with bcrypt."""

    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against a bcrypt hash."""

    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except ValueError:
        return False


def create_token(subject: int, expires_minutes: int, token_type: str) -> str:
    """Create a signed JWT token."""

    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(subject),
        "type": token_type,
        "iat": now,
        "exp": now + timedelta(minutes=expires_minutes),
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_token(token: str, expected_type: str = "access") -> dict:
    """Decode and validate a signed JWT token."""

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
    except jwt.ExpiredSignatureError as exc:
        raise AppException("Token has expired.", status_code=401) from exc
    except jwt.InvalidTokenError as exc:
        raise AppException("Invalid token.", status_code=401) from exc

    if payload.get("type") != expected_type:
        raise AppException("Invalid token type.", status_code=401)

    return payload
