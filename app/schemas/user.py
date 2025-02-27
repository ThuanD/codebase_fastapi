from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing_extensions import Annotated


class UserLoginSchema(BaseModel):
    """Schema for user login."""

    email: str
    username: str


class UserBase(BaseModel):
    """Base schema for user."""

    model_config = ConfigDict(from_attributes=True)
    email: EmailStr = Field(..., description="User email")
    username: str = Field(..., description="Username")
    first_name: str = Field(default="", description="First name")
    last_name: str = Field(default="", description="Last name")
    is_active: bool = Field(default=True, description="Whether the user is active")
    is_superuser: bool = Field(
        default=False, description="Whether the user is a superuser"
    )
    date_joined: datetime = Field(..., description="Date user joined")
    last_login: Optional[datetime] = Field(None, description="Last login datetime")


class UserCreate(UserBase):
    """Schema for creating a user."""

    password: Annotated[str, Field(..., min_length=8, max_length=128)]


class UserUpdate(BaseModel):
    """Schema for updating a user."""

    model_config = ConfigDict(from_attributes=True)
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None


class UserInDBBase(UserBase):
    """Base schema for user in database."""

    id: int = Field(..., description="User ID")
    created_at: datetime = Field(..., description="Creation datetime")
    updated_at: datetime = Field(..., description="Last update datetime")


class User(UserInDBBase):
    """Schema for user response."""

    pass


class UserInDB(UserInDBBase):
    """Schema for user in database with hashed password."""

    password: str = Field(..., description="Hashed password")
