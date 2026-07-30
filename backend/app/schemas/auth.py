"""Pydantic schemas for authentication endpoints."""

from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field

from app.core.constants import UserRole
from app.schemas.user import UserRead


class RegisterRequest(BaseModel):
    """Request body for `POST /auth/register`."""

    full_name: str = Field(..., min_length=1, max_length=255, examples=["Jane Doe"])
    email: EmailStr = Field(..., examples=["jane.doe@example.com"])
    password: str = Field(..., min_length=8, max_length=128, examples=["StrongP@ssw0rd"])
    role: UserRole = Field(default=UserRole.RECRUITER)
    company_name: str | None = Field(default=None, max_length=255, examples=["Acme Corp"])


class LoginRequest(BaseModel):
    """Request body for `POST /auth/login`."""

    email: EmailStr = Field(..., examples=["jane.doe@example.com"])
    password: str = Field(..., min_length=1, examples=["StrongP@ssw0rd"])


class TokenPair(BaseModel):
    """Access + refresh token pair returned on login/refresh."""

    access_token: str = Field(..., description="Short-lived JWT access token.")
    refresh_token: str = Field(..., description="Long-lived JWT refresh token.")
    token_type: str = Field(default="bearer")


class RefreshRequest(BaseModel):
    """Request body for `POST /auth/refresh`."""

    refresh_token: str = Field(..., description="A previously issued, unrevoked refresh token.")


class LogoutRequest(BaseModel):
    """Request body for `POST /auth/logout`."""

    refresh_token: str = Field(..., description="The refresh token to revoke.")


class ForgotPasswordRequest(BaseModel):
    """Request body for `POST /auth/forgot-password`."""

    email: EmailStr = Field(..., examples=["jane.doe@example.com"])


class ResetPasswordRequest(BaseModel):
    """Request body for `POST /auth/reset-password`."""

    reset_token: str = Field(..., description="Token issued via the forgot-password flow.")
    new_password: str = Field(..., min_length=8, max_length=128)


class ChangePasswordRequest(BaseModel):
    """Request body for `POST /auth/change-password`."""

    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8, max_length=128)


class RegisterResponse(BaseModel):
    """Response body for `POST /auth/register`."""

    user: UserRead
    tokens: TokenPair
