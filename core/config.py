"""Application configuration for LectureMind AI."""

import os
from dataclasses import dataclass, field
from typing import Tuple


@dataclass(frozen=True)
class Settings:
    """Central settings loaded from environment variables with safe defaults."""

    app_name: str = "LectureMind AI Backend"
    api_version: str = "1.0.0"
    environment: str = os.getenv("ENVIRONMENT", "development")
    cors_origins: Tuple[str, ...] = field(
        default_factory=lambda: tuple(
            origin.strip()
            for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
            if origin.strip()
        )
    )
    upload_dir: str = os.getenv("UPLOAD_DIR", "../uploads")
    output_dir: str = os.getenv("OUTPUT_DIR", "../outputs")
    allowed_extensions: Tuple[str, ...] = field(
        default_factory=lambda: tuple(
            extension.strip().lower()
            for extension in os.getenv("ALLOWED_EXTENSIONS", ".mp4,.avi,.mov,.mkv").split(",")
            if extension.strip()
        )
    )
    max_upload_size_bytes: int = int(
        os.getenv("MAX_UPLOAD_SIZE_BYTES", str(2 * 1024 * 1024 * 1024))
    )
    whisper_model: str = os.getenv("WHISPER_MODEL", "tiny")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "gemma2:2b")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    answer_similarity_threshold: float = float(
        os.getenv("ANSWER_SIMILARITY_THRESHOLD", "0.30")
    )
    retrieval_similarity_threshold: float = float(
        os.getenv("RETRIEVAL_SIMILARITY_THRESHOLD", "0.3")
    )
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "change-this-secret-in-production")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )
    remember_me_access_token_expire_minutes: int = int(
        os.getenv("REMEMBER_ME_ACCESS_TOKEN_EXPIRE_MINUTES", str(60 * 24 * 7))
    )
    refresh_token_expire_minutes: int = int(
        os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", str(60 * 24 * 30))
    )


settings = Settings()
