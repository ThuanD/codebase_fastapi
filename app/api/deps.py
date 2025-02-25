from typing import AsyncGenerator

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_token
from app.db.session import AsyncSessionLocal
from app.errors.exception import (
    InvalidTokenError,
    NotSuperuserError,
    TokenExpiredError,
    UserIsInactiveError,
    UserNotFoundError,
)
from app.models.user import User
from app.services.users import UserService

security = HTTPBearer()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_current_user(
        session: AsyncSession = Depends(get_db),
        token: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    """Get current user from token."""
    try:
        user_id = verify_token(token.credentials, "access")
        if not user_id:
            raise InvalidTokenError

        user_service = UserService(session)
        user = await user_service.get_by_id(user_id)
        if not user:
            raise UserNotFoundError
        return user
    except TokenExpiredError:
        raise
    except InvalidTokenError:
        raise


async def get_current_active_user(
        current_user: User = Depends(get_current_user)) -> User:
    """Get current active user."""
    if not current_user.is_active:
        raise UserIsInactiveError
    return current_user


async def get_current_active_superuser(
        current_user: User = Depends(get_current_active_user)) -> User:
    """Get current active superuser."""
    if not current_user.is_superuser:
        raise NotSuperuserError
    return current_user
