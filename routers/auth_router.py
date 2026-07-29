"""Authentication API routes."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from dependencies.auth import get_current_user
from services.auth_service import get_profile, login_user, register_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


class RegisterRequest(BaseModel):
    full_name: str
    email: str
    password: str
    confirm_password: str


class LoginRequest(BaseModel):
    email: str
    password: str
    remember_me: bool = False


@router.post("/register")
def register(payload: RegisterRequest):
    """Register a new SaaS user."""

    return register_user(
        payload.full_name,
        payload.email,
        payload.password,
        payload.confirm_password,
    )


@router.post("/login")
def login(payload: LoginRequest):
    """Authenticate a user and issue JWT tokens."""

    return login_user(payload.email, payload.password, payload.remember_me)


@router.get("/me")
def me(current_user=Depends(get_current_user)):
    """Return the authenticated user's profile."""

    return get_profile(current_user["id"])
