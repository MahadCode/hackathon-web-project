"""Application-wide settings for the FastAPI backend.

Centralizes all environment-driven configuration (database URL, JWT
secrets, token lifetimes, CORS origins, allowed hosts) behind a single
cached `Settings` object so no other module reads `os.environ` directly.
"""

from __future__ import annotations

import json
from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def _parse_host_list(value: object) -> list[str]:
    """Accept JSON arrays or comma-separated host/origin strings."""

    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    if not text:
        return []
    if text.startswith("["):
        parsed = json.loads(text)
        return [str(item).strip() for item in parsed if str(item).strip()]
    return [part.strip() for part in text.split(",") if part.strip()]


class Settings(BaseSettings):
    """Typed configuration sourced from environment variables / `.env`."""

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

    frontend_url: str = Field(default="http://localhost:3000", alias="FRONTEND_URL")
    cors_allow_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ],
        alias="CORS_ALLOW_ORIGINS",
    )
    allowed_hosts: list[str] = Field(
        default_factory=lambda: ["localhost", "127.0.0.1", "test", "testserver"],
        alias="ALLOWED_HOSTS",
    )

    upload_dir: str = Field(default="./uploads", alias="UPLOAD_DIR")
    max_upload_size_mb: int = Field(default=10, alias="MAX_UPLOAD_SIZE_MB")

    @field_validator("database_url", mode="before")
    @classmethod
    def async_postgres_url(cls, value: object) -> object:
        if not isinstance(value, str):
            return value
        url = value
        if url.startswith("postgres://"):
            url = "postgresql://" + url[len("postgres://") :]
        if url.startswith("postgresql://") and "+asyncpg" not in url:
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return url

    @field_validator("cors_allow_origins", "allowed_hosts", mode="before")
    @classmethod
    def parse_csv_or_json(cls, value: object) -> list[str]:
        return _parse_host_list(value)

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"

    @property
    def cors_origins(self) -> list[str]:
        origins = list(self.cors_allow_origins)
        frontend = self.frontend_url.rstrip("/")
        if frontend and frontend not in origins:
            origins.append(frontend)
        return origins

    @property
    def trusted_hosts(self) -> list[str]:
        hosts = list(self.allowed_hosts)
        if "*" in hosts:
            return ["*"]
        extras = [
            "localhost",
            "127.0.0.1",
            ".onrender.com",
            ".up.railway.app",
        ]
        for extra in extras:
            if extra not in hosts:
                hosts.append(extra)
        return hosts


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached, process-wide `Settings` instance."""

    return Settings()
