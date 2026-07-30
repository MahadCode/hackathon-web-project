"""Pydantic schemas for candidate resources."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.core.constants import CandidateStatus


class CandidateRead(BaseModel):
    """Public representation of a candidate."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    job_id: uuid.UUID
    full_name: str | None = None
    email: str | None = None
    github_url: str | None = None
    status: CandidateStatus
    parsed_profile: dict[str, Any] | None = None
    match_percentage: float | None = None
    created_at: datetime
    updated_at: datetime
