from typing import Generic, List, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ResponseSchema(BaseModel):
    """Base response schema."""

    code: str = "success"
    message: str = "Success"


class DataResponse(ResponseSchema, Generic[T]):
    """Schema for data response."""

    data: T | None = None


class PaginationParams(BaseModel):
    """Schema for pagination parameters."""

    skip: int = 0
    limit: int = 100


class PaginatedResponse(ResponseSchema, Generic[T]):
    """Schema for paginated response."""

    items: List[T]
    total: int
    skip: int
    limit: int
    has_more: bool
