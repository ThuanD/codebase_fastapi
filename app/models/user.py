from datetime import datetime

from passlib.context import CryptContext
from sqlalchemy import Boolean, Column, DateTime, Integer, String

from app.db.base import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    """User model."""

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, index=True, nullable=False)
    first_name = Column(String(150), nullable=True)
    last_name = Column(String(150), nullable=True)
    email = Column(String(254), unique=True, index=True, nullable=False)
    password = Column(String(128), nullable=False)
    is_superuser = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    date_joined = Column(DateTime, nullable=False, default=datetime.now)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    __tablename__ = "users"
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
    UNUSUAL_PASSWORD = "unusable_password"  # noqa S105

    def __str__(self) -> str:
        """Return the username for this User."""
        return self.get_username()

    def get_username(self) -> str:
        """Return the username for this User."""
        return getattr(self, self.USERNAME_FIELD)

    def get_full_name(self) -> str:
        """Return the first_name plus the last_name, with a space in between."""
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def get_short_name(self) -> str:
        """Return the short name for the user."""
        return self.first_name

    @property
    def is_anonymous(self) -> bool:
        """Always return False."""
        return False

    @property
    def is_authenticated(self) -> bool:
        """Always return True."""
        return True

    def set_password(self, raw_password: str) -> None:
        """Set a user's password."""
        self.password = pwd_context.hash(raw_password)

    def check_password(self, password: str) -> bool:
        """Check a user's password."""
        return pwd_context.verify(password, self.password)

    def set_unusable_password(self) -> None:
        """Set a user's password to an unusable value."""
        self.password = self.UNUSUAL_PASSWORD

    def has_usable_password(self) -> bool:
        """Return False if set_unusable_password() has been called for this user."""
        return self.password == self.UNUSUAL_PASSWORD
