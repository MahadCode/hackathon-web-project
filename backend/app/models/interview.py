"""Interview ORM model — stores generated questions and evaluation results."""

from __future__ import annotations

import uuid

from sqlalchemy import Boolean, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Interview(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """A single automated interview session for a candidate.

    Attributes:
        candidate_id: The candidate who was interviewed.
        questions: List of generated interview questions and metadata,
            stored as JSON (mirrors `InterviewQuestion` from the agent layer).
        overall_assessment: Free-text summary assessment of performance.
        passed: Whether the candidate passed the interview.
    """

    __tablename__ = "interviews"

    candidate_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False
    )
    questions: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    overall_assessment: Mapped[str | None] = mapped_column(Text, nullable=True)
    passed: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    candidate: Mapped["Candidate"] = relationship(back_populates="interviews")
