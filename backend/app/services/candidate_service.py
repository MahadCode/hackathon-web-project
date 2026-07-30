"""Business logic for candidate records."""

from __future__ import annotations

import uuid

from app.core.constants import CandidateStatus
from app.exceptions.errors import NotFoundError
from app.models.candidate import Candidate
from app.repositories.candidate_repository import CandidateRepository


class CandidateService:
    """Coordinates reading and updating `Candidate` records."""

    def __init__(self, candidate_repo: CandidateRepository) -> None:
        """Initialize the service.

        Args:
            candidate_repo: Repository for `Candidate` persistence.
        """

        self._candidate_repo = candidate_repo

    async def get_candidate(self, candidate_id: uuid.UUID) -> Candidate:
        """Fetch a candidate by id.

        Args:
            candidate_id: The candidate's id.

        Returns:
            The matching `Candidate`.

        Raises:
            NotFoundError: If no candidate with this id exists.
        """

        candidate = await self._candidate_repo.get_by_id(candidate_id)
        if candidate is None:
            raise NotFoundError("Candidate not found.")
        return candidate

    async def list_for_job(self, job_id: uuid.UUID, offset: int = 0, limit: int = 20) -> list[Candidate]:
        """List candidates evaluated against a specific job.

        Args:
            job_id: The job to filter candidates by.
            offset: Number of rows to skip.
            limit: Maximum number of rows to return.

        Returns:
            A list of `Candidate` instances.
        """

        return await self._candidate_repo.list_by_job(job_id=job_id, offset=offset, limit=limit)

    async def get_or_create_for_job(self, job_id: uuid.UUID, candidate_id: uuid.UUID | None) -> Candidate:
        """Fetch an existing candidate or create a new one for a job.

        Args:
            job_id: The job the candidate is being evaluated for.
            candidate_id: An existing candidate id to reuse (e.g. when
                uploading a second resume for the same person), or None to
                create a brand-new candidate record.

        Returns:
            The existing or newly created `Candidate`.

        Raises:
            NotFoundError: If `candidate_id` was provided but does not exist.
        """

        if candidate_id is not None:
            return await self.get_candidate(candidate_id)

        candidate = Candidate(job_id=job_id, status=CandidateStatus.NEW)
        return await self._candidate_repo.add(candidate)

    async def update_status(self, candidate: Candidate, status: CandidateStatus) -> Candidate:
        """Update a candidate's pipeline status.

        Args:
            candidate: The candidate to update.
            status: The new status.

        Returns:
            The updated `Candidate`.
        """

        candidate.status = status
        return candidate
