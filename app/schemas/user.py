from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserLoginSchema(BaseModel):
    email: str
    username: str


class UserBase(BaseModel):
    """Base User Schema."""

    email: EmailStr = Field(..., description="User email address")
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    first_name: Optional[str] = Field(None, max_length=150, description="First name")
    last_name: Optional[str] = Field(None, max_length=150, description="Last name")


class UserCreate(UserBase):
    """Schema for creating user."""

    password: str = Field(..., min_length=8, description="User password")


class UserUpdate(BaseModel):
    """Schema for updating user."""

    email: Optional[EmailStr] = Field(None, description="New email address")
    username: Optional[str] = Field(
        None, min_length=3, max_length=50, description="New username"
    )
    password: Optional[str] = Field(None, min_length=8, description="New password")
    first_name: Optional[str] = Field(None, max_length=150, description="First name")
    last_name: Optional[str] = Field(None, max_length=150, description="Last name")


class User(UserBase):
    """Schema for user response."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="User ID")
    is_active: bool = Field(..., description="Whether the user is active")
    is_superuser: bool = Field(..., description="Whether the user is superuser")
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
