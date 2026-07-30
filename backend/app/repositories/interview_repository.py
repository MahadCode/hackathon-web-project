"""Repository for `Interview` persistence operations."""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.interview import Interview
from app.repositories.base import BaseRepository


class InterviewRepository(BaseRepository[Interview]):
    """Data-access operations for `Interview` rows."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the repository.

        Args:
            session: The request-scoped async DB session.
        """

        super().__init__(session=session, model=Interview)

    async def list_by_candidate(self, candidate_id: uuid.UUID) -> list[Interview]:
        """List all interview sessions for a given candidate.

        Args:
            candidate_id: The candidate to filter interviews by.

        Returns:
            A list of matching `Interview` instances.
        """

        result = await self._session.execute(
            select(Interview).where(Interview.candidate_id == candidate_id)
        )
        return list(result.scalars().all())
