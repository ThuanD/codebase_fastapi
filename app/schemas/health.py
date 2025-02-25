from pydantic import BaseModel


class HealthCheckSchema(BaseModel):
    """Schema for health check response."""

    status: str = "healthy"
