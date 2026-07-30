"""Candidate listing/detail endpoints."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query

from app.core.dependencies import get_candidate_service, require_hr
from app.schemas.candidate import CandidateRead
from app.services.candidate_service import CandidateService

router = APIRouter(prefix="/candidates", tags=["Candidates"], dependencies=[Depends(require_hr())])


@router.get(
    "/{candidate_id}",
    response_model=CandidateRead,
    summary="Get a candidate",
    description="Fetches a single candidate's record, including parsed profile and pipeline status.",
    responses={404: {"description": "Candidate not found."}},
)
async def get_candidate(
    candidate_id: uuid.UUID, candidate_service: CandidateService = Depends(get_candidate_service)
) -> CandidateRead:
    """Fetch a single candidate by id.

    Args:
        candidate_id: The candidate's id.
        candidate_service: Injected `CandidateService`.

    Returns:
        The matching candidate record.
    """

    candidate = await candidate_service.get_candidate(candidate_id)
    return CandidateRead.model_validate(candidate)


@router.get(
    "",
    response_model=list[CandidateRead],
    summary="List candidates for a job",
    description="Lists all candidates evaluated against a given job, with pagination.",
)
async def list_candidates_for_job(
    job_id: uuid.UUID = Query(..., description="Job id to list candidates for."),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    candidate_service: CandidateService = Depends(get_candidate_service),
) -> list[CandidateRead]:
    """List candidates evaluated against a specific job.

    Args:
        job_id: The job to filter candidates by.
        offset: Number of rows to skip.
        limit: Maximum number of rows to return.
        candidate_service: Injected `CandidateService`.

    Returns:
        A list of matching candidate records.
    """

    candidates = await candidate_service.list_for_job(job_id=job_id, offset=offset, limit=limit)
    return [CandidateRead.model_validate(candidate) for candidate in candidates]
