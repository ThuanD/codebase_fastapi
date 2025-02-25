from fastapi import status

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_healthcheck(client: AsyncClient):
    """Test healthcheck endpoint."""
    response = await client.get("/api/v1/healthcheck")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "healthy"
