from typing import Optional, Tuple

from sqlalchemy.orm import Session

from app.errors.exception import (
    UserDoesNotExistError,
    UsernameOrEmailAlreadyExistError,
    UsernameOrPasswordIsIncorrectError,
)
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, user_id: int) -> User:
        """Get user by ID."""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise UserDoesNotExistError()
        return user

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.db.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        return self.db.query(User).filter(User.username == username).first()

    def create(self, user_in: UserCreate) -> User:
        """Create new user."""
        if self.get_by_email(user_in.email) or self.get_by_username(user_in.username):
            raise UsernameOrEmailAlreadyExistError()

        user = User(
            email=user_in.email,
            username=user_in.username,
            is_active=True,
        )
        user.set_password(user_in.password)

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user_id: int, user_in: UserUpdate) -> User:
        """Update user information."""
        user = self.get_by_id(user_id)

        update_data = user_in.model_dump(exclude_unset=True)

        if "password" in update_data:
            user.set_password(update_data.pop("password"))

        if "email" in update_data and update_data["email"] != user.email:
            if self.get_by_email(update_data["email"]):
                raise UsernameOrEmailAlreadyExistError()

        if "username" in update_data and update_data["username"] != user.username:
            if self.get_by_username(update_data["username"]):
                raise UsernameOrEmailAlreadyExistError()

        for field, value in update_data.items():
            setattr(user, field, value)

        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user_id: int) -> None:
        """Delete user."""
        user = self.get_by_id(user_id)
        self.db.delete(user)
        self.db.commit()

    def authenticate(self, email: str, password: str) -> User:
        """Authenticate user."""
        user = self.get_by_email(email)
        if not user or not user.check_password(password):
            raise UsernameOrPasswordIsIncorrectError()
        return user

    def get_multi(self, skip: int = 0, limit: int = 100) -> Tuple[list[User], int]:
        """Get multiple users with pagination."""
        query = self.db.query(User)
        total = query.count()
        users = query.offset(skip).limit(limit).all()
        return users, total
