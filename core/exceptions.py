"""Application exceptions and FastAPI handlers."""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from core.logging import get_logger
from utils.responses import error_response

logger = get_logger(__name__)


class AppException(Exception):
    """Base application exception safe to show to API clients."""

    def __init__(self, message: str, status_code: int = 400, error: str | None = None):
        self.message = message
        self.status_code = status_code
        self.error = error or message
        super().__init__(message)


def register_exception_handlers(app: FastAPI) -> None:
    """Register centralized JSON exception handlers."""

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        logger.warning("%s %s failed: %s", request.method, request.url.path, exc.error)
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response(exc.message, exc.error),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning("%s %s validation failed", request.method, request.url.path)
        return JSONResponse(
            status_code=422,
            content=error_response("Validation failed.", exc.errors()),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception("%s %s raised an unexpected error", request.method, request.url.path)
        return JSONResponse(
            status_code=500,
            content=error_response("Internal server error.", "Unexpected server error."),
        )
