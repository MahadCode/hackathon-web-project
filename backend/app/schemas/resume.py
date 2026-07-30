"""Pydantic schemas for resume upload/parsing."""

from __future__ import annotations

import uuid
from typing import Any

from pydantic import BaseModel, Field


class ResumeUploadResponse(BaseModel):
    """Response returned after a resume is uploaded and parsed.

    Attributes:
        resume_id: Id of the persisted `Resume` row.
        candidate_id: Id of the `Candidate` this resume was attached to
            (newly created if this is the candidate's first resume for
            the job).
        parsed_profile: The structured output of the Resume Parser Agent.
    """

    resume_id: uuid.UUID
    candidate_id: uuid.UUID
    parsed_profile: dict[str, Any] = Field(..., description="Structured resume-parse result.")
