"""FastAPI authentication dependencies."""

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.exceptions import AppException
from core.security import decode_token
from managers.user_manager import get_user_by_id

security = HTTPBearer(auto_error=False)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Return the authenticated user from a bearer access token."""

    if credentials is None:
        raise AppException("Authentication required.", status_code=401)

    payload = decode_token(credentials.credentials, expected_type="access")
    user_id = payload.get("sub")

    if user_id is None:
        raise AppException("Invalid token.", status_code=401)

    user = get_user_by_id(int(user_id))

    if user is None:
        raise AppException("Invalid token.", status_code=401)

    return user
