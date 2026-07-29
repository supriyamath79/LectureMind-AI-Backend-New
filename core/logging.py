"""Central logging setup."""

import logging

from core.config import settings


def configure_logging() -> None:
    """Configure application-wide logging once at startup."""

    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def get_logger(name: str) -> logging.Logger:
    """Return a named logger using the central logging configuration."""

    return logging.getLogger(name)
