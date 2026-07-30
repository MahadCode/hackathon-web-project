"""Job posting ORM model."""

from __future__ import annotations

import uuid

from sqlalchemy import Enum as SAEnum, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import JobStatus
from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Job(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """A job posting that candidates are evaluated against.

    Attributes:
        title: Job title, e.g. "Senior Backend Engineer".
        description: Full job description text.
        requirements: Free-text job requirements consumed by the skill
            matching agent.
        status: Current lifecycle status of the posting.
        created_by_id: Id of the `User` (HR staff) who created this job.
    """

    __tablename__ = "jobs"
    __table_args__ = (Index("ix_jobs_status", "status"),)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    requirements: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[JobStatus] = mapped_column(
        SAEnum(JobStatus, name="job_status", create_type=False),
        nullable=False,
        default=JobStatus.DRAFT,
    )
    created_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    created_by: Mapped["User"] = relationship(back_populates="jobs")
    candidates: Mapped[list["Candidate"]] = relationship(
        back_populates="job", cascade="all, delete-orphan"
    )
