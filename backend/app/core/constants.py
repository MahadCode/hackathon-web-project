"""Application-wide constants, primarily role and enum-like definitions.

Using string constants (rather than scattering literal strings across the
codebase) avoids typos causing silent authorization bugs.
"""

from __future__ import annotations

from enum import Enum


class UserRole(str, Enum):
    """Supported user roles for role-based authorization."""

    ADMIN = "ADMIN"
    HR_MANAGER = "HR_MANAGER"
    RECRUITER = "RECRUITER"
    INTERVIEWER = "INTERVIEWER"


class TokenType(str, Enum):
    """Types of JWTs issued by the authentication system."""

    ACCESS = "access"
    REFRESH = "refresh"
    PASSWORD_RESET = "password_reset"


class JobStatus(str, Enum):
    """Lifecycle status of a job posting."""

    DRAFT = "DRAFT"
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    ARCHIVED = "ARCHIVED"


class CandidateStatus(str, Enum):
    """Lifecycle status of a candidate within the hiring pipeline."""

    NEW = "NEW"
    PARSED = "PARSED"
    SHORTLISTED = "SHORTLISTED"
    MANUAL_REVIEW = "MANUAL_REVIEW"
    REJECTED = "REJECTED"
    INTERVIEWING = "INTERVIEWING"
    HIRED = "HIRED"
    NOT_HIRED = "NOT_HIRED"


HR_ROLES: frozenset[UserRole] = frozenset({UserRole.ADMIN, UserRole.HR_MANAGER, UserRole.RECRUITER})
"""Roles permitted to create and manage job postings."""

INTERVIEW_ROLES: frozenset[UserRole] = frozenset(
    {UserRole.ADMIN, UserRole.HR_MANAGER, UserRole.INTERVIEWER, UserRole.RECRUITER}
)
"""Roles permitted to run and evaluate interviews."""
