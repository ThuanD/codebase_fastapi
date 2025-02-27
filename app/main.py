from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from loguru import logger

from app.api import router
from app.core.config import settings
from app.errors.exception import BaseError
from app.errors.exception_hanlder import http_exception_handler
from app.middleware import LoggingMiddleware
from app.utils.logging_config import setup_logging


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan events."""
    # Startup
    setup_logging()
    logger.info("Running application startup tasks...")

    yield

    # Shutdown
    logger.info("Running application shutdown tasks...")


def get_application() -> FastAPI:
    """Create FastAPI application."""
    logger.info("Starting application...")

    application = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        lifespan=lifespan,
    )

    # Add Logging Middleware
    application.add_middleware(LoggingMiddleware)

    # Set CORS middleware
    if settings.ALLOW_ORIGINS:
        application.add_middleware(
            CORSMiddleware,  # type: ignore
            allow_origins=settings.ALLOW_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Add exception handler
    application.add_exception_handler(BaseError, http_exception_handler)  # type: ignore

    # Add routes
    application.include_router(router, prefix=settings.API_V1_STR)

    logger.info("Application startup complete")
    return application


app = get_application()
