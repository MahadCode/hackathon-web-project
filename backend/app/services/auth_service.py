"""Business logic for authentication and account security.

`AuthService` is the only layer that combines password hashing, JWT
issuance, and user/refresh-token persistence into higher-level operations
like "log in" or "rotate a refresh token".
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from app.core.constants import TokenType, UserRole
from app.core.security import (
    TokenPayloadError,
    create_access_token,
    create_password_reset_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.exceptions.errors import AuthenticationError, ConflictError, NotFoundError
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import TokenPair


class AuthService:
    """Coordinates registration, login, token lifecycle, and password resets."""

    def __init__(self, user_repo: UserRepository, refresh_token_repo: RefreshTokenRepository) -> None:
        """Initialize the service.

        Args:
            user_repo: Repository for `User` persistence.
            refresh_token_repo: Repository for `RefreshToken` persistence.
        """

        self._user_repo = user_repo
        self._refresh_token_repo = refresh_token_repo

    async def register(
        self,
        full_name: str,
        email: str,
        password: str,
        role: UserRole,
        company_name: str | None,
    ) -> tuple[User, TokenPair]:
        """Register a new user and issue an initial token pair.

        Args:
            full_name: The new user's display name.
            email: The new user's unique email address.
            password: The new user's plaintext password (hashed before storage).
            role: The role assigned to the new user.
            company_name: Optional company/organization name.

        Returns:
            A tuple of the created `User` and their initial `TokenPair`.

        Raises:
            ConflictError: If a user with this email already exists.
        """

        existing = await self._user_repo.get_by_email(email)
        if existing is not None:
            raise ConflictError("A user with this email already exists.")

        user = User(
            full_name=full_name,
            email=email,
            hashed_password=hash_password(password),
            role=role,
            company_name=company_name,
        )
        user = await self._user_repo.add(user)
        tokens = await self._issue_token_pair(user)
        return user, tokens

    async def login(self, email: str, password: str) -> tuple[User, TokenPair]:
        """Authenticate a user by email/password and issue a token pair.

        Args:
            email: The user's email address.
            password: The user's plaintext password.

        Returns:
            A tuple of the authenticated `User` and a new `TokenPair`.

        Raises:
            AuthenticationError: If credentials are invalid or the account
                is inactive.
        """

        user = await self._user_repo.get_by_email(email)
        if user is None or not verify_password(password, user.hashed_password):
            raise AuthenticationError("Invalid email or password.")
        if not user.is_active:
            raise AuthenticationError("This account has been deactivated.")

        user.last_login = datetime.now(timezone.utc)
        tokens = await self._issue_token_pair(user)
        return user, tokens

    async def refresh(self, refresh_token: str) -> TokenPair:
        """Rotate a refresh token: revoke the old one and issue a new pair.

        Args:
            refresh_token: A previously issued refresh token string.

        Returns:
            A new `TokenPair`.

        Raises:
            AuthenticationError: If the token is invalid, expired, revoked,
                or belongs to a user that no longer exists/is inactive.
        """

        try:
            payload = decode_token(refresh_token, expected_type=TokenType.REFRESH)
        except TokenPayloadError as exc:
            raise AuthenticationError("Invalid or expired refresh token.") from exc

        stored_token = await self._refresh_token_repo.get_by_jti(payload["jti"])
        if stored_token is None or stored_token.is_revoked:
            raise AuthenticationError("Refresh token has been revoked.")

        user = await self._user_repo.get_by_id(uuid.UUID(payload["sub"]))
        if user is None or not user.is_active:
            raise AuthenticationError("User not found or inactive.")

        await self._refresh_token_repo.revoke(stored_token)
        return await self._issue_token_pair(user)

    async def logout(self, refresh_token: str) -> None:
        """Revoke a single refresh token (log out of one session).

        Args:
            refresh_token: The refresh token string to revoke.

        Raises:
            AuthenticationError: If the token is malformed.
        """

        try:
            payload = decode_token(refresh_token, expected_type=TokenType.REFRESH)
        except TokenPayloadError as exc:
            raise AuthenticationError("Invalid refresh token.") from exc

        stored_token = await self._refresh_token_repo.get_by_jti(payload["jti"])
        if stored_token is not None:
            await self._refresh_token_repo.revoke(stored_token)

    async def request_password_reset(self, email: str) -> str | None:
        """Issue a password reset token for a user, if the email is known.

        Args:
            email: The email address requesting a reset.

        Returns:
            The reset token if the email matches an active user, otherwise
            None. Callers should return the same generic success response
            in both cases to avoid leaking which emails are registered.
        """

        user = await self._user_repo.get_by_email(email)
        if user is None:
            return None
        return create_password_reset_token(str(user.id))

    async def reset_password(self, reset_token: str, new_password: str) -> None:
        """Reset a user's password using a valid password-reset token.

        Args:
            reset_token: The token issued via `request_password_reset`.
            new_password: The new plaintext password to set.

        Raises:
            AuthenticationError: If the token is invalid or expired.
            NotFoundError: If the associated user no longer exists.
        """

        try:
            payload = decode_token(reset_token, expected_type=TokenType.PASSWORD_RESET)
        except TokenPayloadError as exc:
            raise AuthenticationError("Invalid or expired password reset token.") from exc

        user = await self._user_repo.get_by_id(uuid.UUID(payload["sub"]))
        if user is None:
            raise NotFoundError("User not found.")

        user.hashed_password = hash_password(new_password)
        await self._refresh_token_repo.revoke_all_for_user(user.id)

    async def change_password(self, user: User, current_password: str, new_password: str) -> None:
        """Change a logged-in user's password after verifying the current one.

        Args:
            user: The authenticated user changing their password.
            current_password: The user's current plaintext password.
            new_password: The new plaintext password to set.

        Raises:
            AuthenticationError: If `current_password` does not match.
        """

        if not verify_password(current_password, user.hashed_password):
            raise AuthenticationError("Current password is incorrect.")

        user.hashed_password = hash_password(new_password)
        await self._refresh_token_repo.revoke_all_for_user(user.id)

    async def _issue_token_pair(self, user: User) -> TokenPair:
        """Create a new access/refresh token pair and persist the refresh token.

        Args:
            user: The user to issue tokens for.

        Returns:
            A `TokenPair` containing both tokens.
        """

        access_token = create_access_token(user_id=str(user.id), role=user.role.value)
        refresh_token_str = create_refresh_token(user_id=str(user.id))

        payload = decode_token(refresh_token_str, expected_type=TokenType.REFRESH)
        refresh_token_record = RefreshToken(
            user_id=user.id,
            jti=payload["jti"],
            expires_at=datetime.fromtimestamp(payload["exp"], tz=timezone.utc),
        )
        await self._refresh_token_repo.add(refresh_token_record)

        return TokenPair(access_token=access_token, refresh_token=refresh_token_str)
