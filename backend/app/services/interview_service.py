"""Business logic for interview question generation and evaluation.

Question generation reuses `InterviewAgent.next_question` directly, as
specified. Transcript evaluation has no dedicated agent in the AI layer
(only one-question-at-a-time generation exists there), so this service
adds a thin, separately-defined evaluation step using the same shared
Gemini client and the `InterviewResult` schema already defined in the
agent layer's `utils.schemas` module — no agent or graph logic is
duplicated or regenerated.
"""

from __future__ import annotations

import uuid

from ai_agents.agents.interview_agent import InterviewAgent
from ai_agents.config.llm import get_gemini_llm
from ai_agents.utils.schemas import InterviewResult
from app.exceptions.errors import NotFoundError
from app.models.candidate import Candidate
from app.models.interview import Interview
from app.repositories.candidate_repository import CandidateRepository
from app.repositories.interview_repository import InterviewRepository
from app.schemas.interview import InterviewQuestionResponse

_EVALUATION_SYSTEM_PROMPT: str = """You are an expert technical interviewer reviewing a completed
interview transcript.

Given the full list of questions and answers, assess the candidate's overall performance and
decide whether they passed. Return ONLY the structured output described by the response schema.
"""


class InterviewService:
    """Coordinates adaptive question generation and transcript evaluation."""

    def __init__(
        self,
        candidate_repo: CandidateRepository,
        interview_repo: InterviewRepository,
        interview_agent: InterviewAgent | None = None,
    ) -> None:
        """Initialize the service.

        Args:
            candidate_repo: Repository for `Candidate` persistence.
            interview_repo: Repository for `Interview` persistence.
            interview_agent: Optional agent override, primarily for testing.
        """

        self._candidate_repo = candidate_repo
        self._interview_repo = interview_repo
        self._interview_agent = interview_agent or InterviewAgent()

    async def next_question(
        self, candidate_id: uuid.UUID, job_description: str, conversation_history: list[str]
    ) -> InterviewQuestionResponse:
        """Generate the next adaptive interview question for a candidate.

        Args:
            candidate_id: The candidate being interviewed.
            job_description: The job description to ground the question in.
            conversation_history: Prior Q&A turns, oldest first.

        Returns:
            The next question to ask, as an `InterviewQuestionResponse`.

        Raises:
            NotFoundError: If the candidate does not exist or has not been parsed.
        """

        candidate = await self._get_parsed_candidate(candidate_id)
        skills = list((candidate.parsed_profile or {}).get("skills") or [])
        weaknesses = list((candidate.parsed_profile or {}).get("missing_skills") or [])

        question = self._interview_agent.next_question(
            job_description=job_description,
            candidate_skills=skills,
            candidate_weaknesses=weaknesses,
            conversation_history=conversation_history,
        )
        return InterviewQuestionResponse(
            question=question.question,
            focus_area=question.focus_area,
            is_follow_up=question.is_follow_up,
        )

    async def evaluate_transcript(self, candidate_id: uuid.UUID, questions_and_answers: list[str]) -> Interview:
        """Evaluate a completed interview transcript and persist the result.

        Args:
            candidate_id: The candidate whose interview is being evaluated.
            questions_and_answers: The full Q&A transcript, as strings.

        Returns:
            The persisted `Interview` record.

        Raises:
            NotFoundError: If the candidate does not exist.
        """

        candidate = await self._candidate_repo.get_by_id(candidate_id)
        if candidate is None:
            raise NotFoundError("Candidate not found.")

        result = self._run_evaluation(questions_and_answers)

        interview = Interview(
            candidate_id=candidate.id,
            questions=None,
            overall_assessment=result.overall_assessment,
            passed=result.passed,
        )
        return await self._interview_repo.add(interview)

    def _run_evaluation(self, questions_and_answers: list[str]) -> InterviewResult:
        """Invoke the shared LLM to evaluate a transcript against `InterviewResult`.

        Args:
            questions_and_answers: The full Q&A transcript, as strings.

        Returns:
            A validated `InterviewResult`.
        """

        llm = get_gemini_llm()
        structured_llm = llm.with_structured_output(InterviewResult)
        transcript = "\n".join(questions_and_answers)
        return structured_llm.invoke(
            [
                ("system", _EVALUATION_SYSTEM_PROMPT),
                ("human", f"Interview transcript:\n---\n{transcript}\n---\n\nEvaluate this interview."),
            ]
        )

    async def _get_parsed_candidate(self, candidate_id: uuid.UUID) -> Candidate:
        """Fetch a candidate and ensure it has been parsed.

        Args:
            candidate_id: The candidate's id.

        Returns:
            The matching, parsed `Candidate`.

        Raises:
            NotFoundError: If the candidate does not exist or lacks a
                parsed profile.
        """

        candidate = await self._candidate_repo.get_by_id(candidate_id)
        if candidate is None:
            raise NotFoundError("Candidate not found.")
        if candidate.parsed_profile is None:
            raise NotFoundError("Candidate has not been parsed yet.")
        return candidate
