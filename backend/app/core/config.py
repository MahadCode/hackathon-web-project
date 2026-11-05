"""Application-wide settings for the FastAPI backend.

Centralizes all environment-driven configuration (database URL, JWT
secrets, token lifetimes, CORS origins) behind a single cached
`Settings` object so no other module reads `os.environ` directly.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed configuration sourced from environment variables / `.env`.

    Attributes:
        app_name: Human-readable application name shown in API docs.
        environment: Deployment environment name (e.g. "development",
            "production"); used to toggle debug behavior.
        api_v1_prefix: URL prefix under which all v1 routes are mounted.
        database_url: Async SQLAlchemy connection string, e.g.
            "postgresql+asyncpg://user:pass@host:5432/dbname".
        jwt_secret_key: Secret used to sign JWT access/refresh tokens.
            Must be overridden via environment variable in every real
            deployment; never commit a real value.
        jwt_algorithm: Signing algorithm for JWTs.
        access_token_expire_minutes: Access token lifetime in minutes.
        refresh_token_expire_days: Refresh token lifetime in days.
        password_reset_token_expire_minutes: Lifetime of a password reset
            token in minutes.
        cors_allow_origins: List of origins permitted by CORS middleware.
        upload_dir: Filesystem directory where uploaded files (resumes,
            profile images) are stored.
        max_upload_size_mb: Maximum accepted upload size, in megabytes.
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = Field(default="Hiring AI Backend")
    environment: str = Field(default="development", alias="ENVIRONMENT")
    api_v1_prefix: str = Field(default="/api/v1")

    database_url: str = Field(
        default="sqlite+aiosqlite:///./hiring_ai.sqlite",
        alias="DATABASE_URL",
    )

    jwt_secret_key: str = Field(..., alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(default=7, alias="REFRESH_TOKEN_EXPIRE_DAYS")
    password_reset_token_expire_minutes: int = Field(
        default=30, alias="PASSWORD_RESET_TOKEN_EXPIRE_MINUTES"
    )

    cors_allow_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ]
    )

    upload_dir: str = Field(default="./uploads", alias="UPLOAD_DIR")
    max_upload_size_mb: int = Field(default=10, alias="MAX_UPLOAD_SIZE_MB")

    @property
    def is_production(self) -> bool:
        """Whether the app is running in a production environment.

        Returns:
            True if `environment` equals "production" (case-insensitive).
        """

        return self.environment.lower() == "production"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached, process-wide `Settings` instance.

    Returns:
        The singleton `Settings` instance for this process.
    """

    return Settings()
