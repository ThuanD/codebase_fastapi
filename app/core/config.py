from pathlib import Path
from typing import List

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Application settings."""

    API_V1_STR: str = Field("/api/v1", description="API v1 url")
    PROJECT_NAME: str = Field("FastAPI Project", description="Project name")

    # CORS
    ALLOW_ORIGINS: List[str] = Field(..., description="List of allowed origins")

    # Security
    SECRET_KEY: SecretStr = Field(..., description="Secret key for FastAPI project")
    SECURITY_ALGORITHM: str = Field("HS256", description="Security algorithm")
    ACCESS_TOKEN_EXPIRE_SECONDS: int = Field(
        86400,  # 24 hours
        description="Access token expiration in seconds",
    )
    REFRESH_TOKEN_EXPIRE_SECONDS: int = Field(
        604800,  # 7 days
        description="Refresh token expiration in seconds",
    )

    DATABASE_URL: str = Field("postgresql://postgres:postgres@localhost:5432/app")
    ASYNC_DATABASE_URL: str = Field(
        "postgresql+asyncpg://postgres:postgres@localhost:5432/app"
    )

    # Logging
    LOG_LEVEL: str = Field("INFO", description="Logging level")
    LOG_FORMAT: str = Field(
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>",
        description="Logging format",
    )

    class Config:
        """Configuration for environment variables and case sensitivity."""

        case_sensitive = False
        env_file = ".env"
        extra = "allow"


settings = Settings()
