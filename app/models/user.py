from datetime import UTC, datetime
from typing import Optional

from passlib.context import CryptContext
from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    """User model."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(150), default="")
    last_name: Mapped[Optional[str]] = mapped_column(String(150), default="")
    email: Mapped[str] = mapped_column(String(254), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(128))
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_staff: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
    UNUSUAL_PASSWORD = "unusable_password"  # noqa S105

    def __str__(self) -> str:
        """Return string representation of user.

        Returns:
            Username

        """
        return self.get_username()

    def get_username(self) -> str:
        """Get username.

        Returns:
            Username

        """
        return getattr(self, self.USERNAME_FIELD)

    def get_full_name(self) -> str:
        """Get full name.

        Returns:
            Full name (first name + last name)

        """
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def get_short_name(self) -> str:
        """Get short name.

        Returns:
            First name

        """
        return self.first_name or ""

    @property
    def is_anonymous(self) -> bool:
        """Check if user is anonymous.

        Returns:
            Always False for real users

        """
        return False

    @property
    def is_authenticated(self) -> bool:
        """Check if user is authenticated.

        Returns:
            Always True for real users

        """
        return True

    def set_password(self, password: str) -> None:
        """Set password.

        Args:
            password: Plain text password

        """
        self.password = pwd_context.hash(password)

    def check_password(self, password: str) -> bool:
        """Check if password is correct.

        Args:
            password: Plain text password to check

        Returns:
            True if password is correct, False otherwise

        """
        return pwd_context.verify(password, self.password)

    def set_unusable_password(self) -> None:
        """Set a user's password to an unusable value."""
        self.password = self.UNUSUAL_PASSWORD

    def has_usable_password(self) -> bool:
        """Return False if set_unusable_password() has been called for this user."""
        return self.password == self.UNUSUAL_PASSWORD
