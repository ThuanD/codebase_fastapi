from datetime import datetime

from fastapi import HTTPException, status

from sqlalchemy.orm import Session

from app.core.security import create_token, verify_token
from app.errors.exception import (
    EmailAlreadyExistError,
    UserIsInactiveError,
    UsernameAlreadyExistError,
    UsernameOrPasswordIsIncorrectError,
)
from app.models.user import User
from app.schemas.auth import RegisterRequest, TokenResponse
from app.services.users import UserService


class AuthService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.user_service = UserService(db)

    def register(self, register_data: RegisterRequest) -> User:
        email = str(register_data.email)

        # Check if username or email already exists
        if self.user_service.get_by_email(email):
            raise EmailAlreadyExistError
        if self.user_service.get_by_username(register_data.username):
            raise UsernameAlreadyExistError

        # Create user object from register data
        user = User(
            email=email,
            username=register_data.username,
            first_name=register_data.first_name,
            last_name=register_data.last_name,
            is_active=True,
            date_joined=datetime.now(),
        )
        user.set_password(register_data.password)

        # Save to database
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def login(self, email: str, password: str) -> TokenResponse:
        user = self.user_service.authenticate(email=email, password=password)

        if not user:
            raise UsernameOrPasswordIsIncorrectError
        if not user.is_active:
            raise UserIsInactiveError

        # Update last login
        user.last_login = datetime.now()
        self.db.commit()

        return TokenResponse(
            access_token=create_token(user.id, "access"),
            refresh_token=create_token(user.id, "refresh"),
        )

    def refresh_token(self, refresh_token: str) -> TokenResponse:
        user_id = verify_token(refresh_token, "refresh")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = self.user_service.get_by_id(int(user_id))
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return TokenResponse(
            access_token=create_token(user.id, "access"),
            refresh_token=create_token(user.id, "refresh"),
        )

    def logout(self, user):
        # In a real application, you might want to:
        # 1. Add the token to a blacklist
        # 2. Clear any user sessions
        # 3. Clear any cached user data
        return {"message": "Successfully logged out"}
