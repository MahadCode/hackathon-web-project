"""FastAPI application factory and entrypoint.

Run with: `uvicorn app.main:app --reload`
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging, get_logger
from app.database.base import Base
from app.database.session import engine
from app.exceptions.handlers import register_exception_handlers
from app.middleware.cors import add_cors_middleware
from app.middleware.logging_middleware import RequestLoggingMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware
import app.models  # noqa: F401 — register ORM tables on Base.metadata

configure_logging()
logger = get_logger(__name__, component="startup")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup/shutdown resources.

    Args:
        app: The FastAPI application instance.

    Yields:
        Control back to FastAPI while the app is running.
    """

    logger.info("Application starting up.")
    settings = get_settings()
    if settings.database_url.startswith("sqlite"):
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
        logger.info("SQLite schema is ready.")
    yield
    logger.info("Application shutting down.")
    await engine.dispose()


def create_app() -> FastAPI:
    """Construct and configure the FastAPI application.

    Returns:
        A fully configured `FastAPI` instance.
    """

    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        description="Enterprise hiring platform backend: authentication, job/candidate "
        "management, and an AI-powered LangGraph evaluation workflow.",
        version="1.0.0",
        lifespan=lifespan,
    )

    add_cors_middleware(app)
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RequestLoggingMiddleware)

    register_exception_handlers(app)

    app.include_router(api_router, prefix=settings.api_v1_prefix)

    return app


app: FastAPI = create_app()
