from typing import Any

from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_superuser, get_current_active_user, get_db
from app.errors.exception import UserNotFoundError
from app.models.user import User
from app.schemas.common import PaginatedResponse
from app.schemas.user import User as UserSchema
from app.schemas.user import UserCreate, UserUpdate
from app.services.users import UserService

router = APIRouter()


@router.post(
    "",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create new user",
    description="Create new user with email and username. "
                "Only superuser can create new users.",
)
async def create_user(
        user_in: UserCreate,
        db: AsyncSession = Depends(get_db),
        _current_user: User = Depends(get_current_active_superuser),
) -> UserSchema:
    """Create a new user."""
    user_service = UserService(db)
    return await user_service.create(user_in)


@router.get(
    "/me",
    response_model=UserSchema,
    summary="Get current user info",
    description="Get information about currently logged in user.",
)
async def read_user_me(
        current_user: User = Depends(get_current_active_user)) -> UserSchema:
    """Read current user information."""
    return current_user


@router.patch(
    "/me",
    response_model=UserSchema,
    summary="Update current user",
    description="Update information for currently logged in user.",
)
async def update_user_me(
        user_in: UserUpdate,
        current_user: User = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_db),
) -> UserSchema:
    """Update current user information."""
    user_service = UserService(db)
    return await user_service.update(current_user.id, user_in)


@router.get(
    "/{user_id}",
    response_model=UserSchema,
    summary="Get user by ID",
    description="Get user information by ID. "
                "Only superuser can access other users' info.",
)
async def read_user_by_id(
        user_id: int,
        db: AsyncSession = Depends(get_db),
        _current_user: User = Depends(get_current_active_superuser),
) -> UserSchema:
    """Read user by ID."""
    user_service = UserService(db)
    user = await user_service.get_by_id(user_id)
    if not user:
        raise UserNotFoundError
    return user


@router.get(
    "",
    response_model=PaginatedResponse[UserSchema],
    summary="Get all users",
    description="Get list of users with pagination. "
                "Only superuser can access this endpoint.",
)
async def read_users(
        db: AsyncSession = Depends(get_db),
        _current_user: User = Depends(get_current_active_superuser),
        skip: int = 0,
        limit: int = 100,
) -> dict[str, Any]:
    """Read all users with pagination."""
    user_service = UserService(db)
    users, total = await user_service.get_multi(skip=skip, limit=limit)
    return {
        "items": users,
        "total": total,
        "skip": skip,
        "limit": limit,
        "has_more": total > (skip + limit),
    }


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
        user_id: int,
        db: AsyncSession = Depends(get_db),
        _current_user: User = Depends(get_current_active_superuser),
) -> None:
    """Delete user by ID."""
    user_service = UserService(db)
    await user_service.delete(user_id)
