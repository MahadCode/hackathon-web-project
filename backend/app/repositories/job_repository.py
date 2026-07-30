"""Repository for `Job` persistence operations."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import JobStatus
from app.models.job import Job
from app.repositories.base import BaseRepository


class JobRepository(BaseRepository[Job]):
    """Data-access operations for `Job` rows."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the repository.

        Args:
            session: The request-scoped async DB session.
        """

        super().__init__(session=session, model=Job)

    async def list_by_status(
        self, status: JobStatus | None = None, offset: int = 0, limit: int = 100
    ) -> list[Job]:
        """List jobs, optionally filtered by status.

        Args:
            status: If provided, only jobs with this status are returned.
            offset: Number of rows to skip.
            limit: Maximum number of rows to return.

        Returns:
            A list of matching `Job` instances.
        """

        query = select(Job)
        if status is not None:
            query = query.where(Job.status == status)
        query = query.offset(offset).limit(limit)
        result = await self._session.execute(query)
        return list(result.scalars().all())
