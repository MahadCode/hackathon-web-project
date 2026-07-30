"""Candidate ORM model."""

from __future__ import annotations

import uuid

from sqlalchemy import Enum as SAEnum, Float, ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import CandidateStatus
from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Candidate(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """A candidate evaluated against a specific `Job`.

    Attributes:
        job_id: The job this candidate is being evaluated for.
        full_name: Candidate's name, populated once parsed.
        email: Candidate's email, populated once parsed.
        github_url: Candidate's GitHub profile URL, if provided/extracted.
        status: Current stage of the candidate in the hiring pipeline.
        parsed_profile: Full structured resume-parse output, stored as JSON
            for auditability (mirrors `ParsedCandidate` from the agent layer).
        match_percentage: Cached skill-match percentage for quick listing/
            sorting without re-joining to the `Score` table.
    """

    __tablename__ = "candidates"
    __table_args__ = (Index("ix_candidates_job_status", "job_id", "status"),)

    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False
    )
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email: Mapped[str | None] = mapped_column(String(320), nullable=True, index=True)
    github_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    status: Mapped[CandidateStatus] = mapped_column(
        SAEnum(CandidateStatus, name="candidate_status", create_type=False),
        nullable=False,
        default=CandidateStatus.NEW,
    )
    parsed_profile: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    match_percentage: Mapped[float | None] = mapped_column(Float, nullable=True)

    job: Mapped["Job"] = relationship(back_populates="candidates")
    resumes: Mapped[list["Resume"]] = relationship(back_populates="candidate", cascade="all, delete-orphan")
    interviews: Mapped[list["Interview"]] = relationship(
        back_populates="candidate", cascade="all, delete-orphan"
    )
    scores: Mapped[list["Score"]] = relationship(back_populates="candidate", cascade="all, delete-orphan")
    email_logs: Mapped[list["EmailLog"]] = relationship(
        back_populates="candidate", cascade="all, delete-orphan"
    )
