"""Pydantic schemas for job resources."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.constants import JobStatus


class JobCreate(BaseModel):
    """Request body for `POST /jobs`."""

    title: str = Field(..., min_length=1, max_length=255, examples=["Senior Backend Engineer"])
    description: str = Field(..., min_length=1, examples=["We are looking for..."])
    requirements: str = Field(..., min_length=1, examples=["5+ years Python, PostgreSQL, AWS"])
    status: JobStatus = Field(default=JobStatus.DRAFT)


class JobUpdate(BaseModel):
    """Request body for `PUT /jobs/{id}`. All fields optional (partial update)."""

    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, min_length=1)
    requirements: str | None = Field(default=None, min_length=1)
    status: JobStatus | None = None


class JobRead(BaseModel):
    """Public representation of a job posting."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    description: str
    requirements: str
    status: JobStatus
    created_by_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
