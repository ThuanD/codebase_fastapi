import logging
import sys
from typing import Any, Dict, Optional

from loguru import logger

from app.core.config import settings


class InterceptHandler(logging.Handler):
    """Intercept standard logging and redirect to loguru."""

    def emit(self, record: logging.LogRecord) -> None:
        """Intercept and emit log record."""
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back  # type: ignore
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging(_logging_config: Optional[Dict[str, Any]] = None) -> None:
    """Configure logging with loguru."""
    logger.remove()

    logger.add(
        sys.stdout,
        format=settings.LOG_FORMAT,
        level=settings.LOG_LEVEL,
        serialize=True,
    )

    logger.add(
        "logs/app.log",
        format=settings.LOG_FORMAT,
        level="ERROR",
        rotation="500 MB",
        retention="10 days",
    )

    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
