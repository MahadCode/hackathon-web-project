"""Top-level API router aggregating all versioned route modules."""

from __future__ import annotations

from fastapi import APIRouter

from app.api.routes import auth, candidates, health, interviews, jobs, resumes, users, workflow

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(jobs.router)
api_router.include_router(candidates.router)
api_router.include_router(resumes.router)
api_router.include_router(interviews.router)
api_router.include_router(workflow.router)
