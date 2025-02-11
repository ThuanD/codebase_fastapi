from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from sqlalchemy.orm import Session

from app.core.security import verify_token
from app.db.session import SessionLocal
from app.errors.exception import (
    InvalidTokenError,
    NotSuperuserError,
    TokenExpiredError,
    UnauthorizedError,
    UserIsInactiveError,
)
from app.models.user import User
from app.services.users import UserService

security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    """Get current user from token."""
    try:
        user_id = verify_token(token.credentials)
        if not user_id:
            raise UnauthorizedError(message="Could not validate credentials")

        user_service = UserService(db)
        user = user_service.get_by_id(int(user_id))
        if not user:
            raise UnauthorizedError(message="User not found")

        return user
    except TokenExpiredError:
        raise UnauthorizedError(message="Token has expired")
    except InvalidTokenError as e:
        raise UnauthorizedError(message=str(e))


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise UserIsInactiveError()
    return current_user


def get_current_active_superuser(
    current_user: User = Depends(get_current_active_user),
) -> User:
    if not current_user.is_superuser:
        raise NotSuperuserError()
    return current_user
