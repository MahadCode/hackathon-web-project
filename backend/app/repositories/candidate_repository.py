"""Repository for `Candidate` persistence operations."""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.candidate import Candidate
from app.repositories.base import BaseRepository


class CandidateRepository(BaseRepository[Candidate]):
    """Data-access operations for `Candidate` rows."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the repository.

        Args:
            session: The request-scoped async DB session.
        """

        super().__init__(session=session, model=Candidate)

    async def list_by_job(self, job_id: uuid.UUID, offset: int = 0, limit: int = 100) -> list[Candidate]:
        """List candidates evaluated against a specific job.

        Args:
            job_id: The job to filter candidates by.
            offset: Number of rows to skip.
            limit: Maximum number of rows to return.

        Returns:
            A list of matching `Candidate` instances.
        """

        query = select(Candidate).where(Candidate.job_id == job_id).offset(offset).limit(limit)
        result = await self._session.execute(query)
        return list(result.scalars().all())
