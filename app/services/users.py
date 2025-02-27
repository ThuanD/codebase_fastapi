from typing import Optional, Tuple

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.errors.exception import (
    UsernameOrEmailAlreadyExistError,
    UsernameOrPasswordIsIncorrectError,
    UserNotFoundError,
)
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """Service for user operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize UserService."""
        self.db = db

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        result = await self.db.execute(select(User).filter(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = await self.db.execute(select(User).filter(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        result = await self.db.execute(select(User).filter(User.username == username))
        return result.scalar_one_or_none()

    async def create(self, user_in: UserCreate) -> User:
        """Create a new user."""
        if await self.get_by_email(str(user_in.email)):
            raise UsernameOrEmailAlreadyExistError
        if await self.get_by_username(user_in.username):
            raise UsernameOrEmailAlreadyExistError

        user = User(**user_in.model_dump(exclude={"password"}))
        user.set_password(user_in.password)

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update(self, user_id: int, user_in: UserUpdate) -> User:
        """Update user information."""
        user = await self.get_by_id(user_id)
        if not user:
            raise UserNotFoundError

        update_data = user_in.model_dump(exclude_unset=True)

        if "password" in update_data:
            user.set_password(update_data.pop("password"))

        if "email" in update_data and update_data["email"] != user.email:
            if await self.get_by_email(update_data["email"]):
                raise UsernameOrEmailAlreadyExistError

        if "username" in update_data and update_data["username"] != user.username:
            if await self.get_by_username(update_data["username"]):
                raise UsernameOrEmailAlreadyExistError

        for field, value in update_data.items():
            setattr(user, field, value)

        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete(self, user_id: int) -> None:
        """Delete user."""
        user = await self.get_by_id(user_id)
        if not user:
            raise UserNotFoundError

        await self.db.delete(user)
        await self.db.commit()

    async def authenticate(self, email: str, password: str) -> Optional[User]:
        """Authenticate user."""
        user = await self.get_by_email(email)
        if not user or not user.check_password(password):
            raise UsernameOrPasswordIsIncorrectError
        return user

    async def get_multi(
        self, skip: int = 0, limit: int = 100
    ) -> Tuple[list[User], int]:
        """Get multiple users with pagination."""
        query = select(User).offset(skip).limit(limit)
        result = await self.db.execute(query)
        users = result.scalars().all()
        total = await self.db.execute(select(func.count(User.id)))
        total_count = total.scalar()
        return list(users), total_count
