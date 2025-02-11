from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from loguru import logger
from starlette.middleware.cors import ALL_METHODS, SAFELISTED_HEADERS

from app.api import router
from app.core.config import settings
from app.errors.exception import BaseError
from app.errors.exception_hanlder import http_exception_handler
from app.utils.logging_config import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    setup_logging()
    logger.info("Running application startup tasks...")

    yield  # This line separates startup from shutdown events

    # Shutdown
    logger.info("Running application shutdown tasks...")


def get_application() -> FastAPI:
    logger.info("Starting application...")

    application = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        lifespan=lifespan,
    )

    # Log middleware setup
    logger.info("Configuring middleware...")
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOW_ORIGINS,
        allow_credentials=True,
        allow_methods=ALL_METHODS,
        allow_headers=SAFELISTED_HEADERS,
    )

    application.include_router(router, prefix=settings.API_V1_STR)
    application.add_exception_handler(BaseError, http_exception_handler)

    logger.info("Application startup complete")
    return application


app = get_application()


@app.get("/")
async def root():
    return {"message": "Hello World"}
