from typing import Any

from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session

from app.api.deps import get_current_active_superuser, get_current_active_user, get_db
from app.schemas.common import PaginatedResponse
from app.schemas.user import User, UserCreate, UserUpdate
from app.services.users import UserService

router = APIRouter()


@router.post(
    "",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Create new user",
    description="Create new user with email and username. Only superuser can create new users.",
)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> User:
    """Create new user with the following information:
    - **email**: unique email address
    - **username**: unique username
    - **password**: strong password
    """
    user_service = UserService(db)
    return user_service.create(user_in)


@router.get(
    "/me",
    response_model=User,
    summary="Get current user info",
    description="Get information about currently logged in user.",
)
def read_user_me(current_user: User = Depends(get_current_active_user)) -> User:
    """Get current user information."""
    return current_user


@router.patch(
    "/me",
    response_model=User,
    summary="Update current user",
    description="Update information for currently logged in user.",
)
def update_user_me(
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> User:
    """Update current user information:
    - **email**: new email address
    - **username**: new username
    - **password**: new password
    - **first_name**: first name
    - **last_name**: last name
    """
    user_service = UserService(db)
    return user_service.update(current_user.id, user_in)


@router.get(
    "/{user_id}",
    response_model=User,
    summary="Get user by ID",
    description="Get user information by ID. Only superuser can access other users' information.",
)
def read_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> User:
    """Get user by ID. Only superuser can access this endpoint."""
    user_service = UserService(db)
    return user_service.get_by_id(user_id)


@router.get(
    "",
    response_model=PaginatedResponse[User],
    summary="Get all users",
    description="Get list of users with pagination. Only superuser can access this endpoint.",
)
def read_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
    skip: int = 0,
    limit: int = 100,
) -> dict[str:Any]:
    """Get all users with pagination. Only superuser can access this endpoint.

    Parameters
    ----------
    - **skip**: number of records to skip
    - **limit**: maximum number of records to return

    """
    user_service = UserService(db)
    users, total = user_service.get_multi(skip=skip, limit=limit)

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
    summary="Delete user",
    description="Delete user by ID. Only superuser can delete users.",
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> None:
    """Delete user by ID. Only superuser can access this endpoint."""
    user_service = UserService(db)
    user_service.delete(user_id)
