from datetime import datetime

from fastapi import status

import pytest
from httpx import AsyncClient

from app.errors.error_code import ErrorCode
from app.models.user import User

API_USERS_ENDPOINT = "/api/v1/users"
API_ME_ENDPOINT = "/api/v1/users/me"


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient, superuser_token_headers: dict):
    """Test creating a new user."""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123",  # NOSONAR
        "first_name": "",
        "last_name": "",
        "is_active": True,
        "date_joined": datetime.utcnow().isoformat(),
    }
    response = await client.post(
        API_USERS_ENDPOINT,
        headers=superuser_token_headers,
        json=user_data,
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"


@pytest.mark.asyncio
async def test_get_user(
    client: AsyncClient, superuser_token_headers: dict, normal_user: User
):
    """Test getting a user by ID."""
    response = await client.get(
        f"/api/v1/users/{normal_user.id}", headers=superuser_token_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == normal_user.email
    assert data["username"] == normal_user.username


@pytest.mark.asyncio
async def test_get_nonexistent_user(
    client: AsyncClient, nonexistent_user_token_headers: dict, normal_user: User
):
    """Test getting a user by ID."""
    response = await client.get(
        f"/api/v1/users/{normal_user.id}", headers=nonexistent_user_token_headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["code"] == ErrorCode.USER_DOES_NOT_EXIST_CODE


@pytest.mark.asyncio
async def test_create_user_success(client: AsyncClient, superuser_token_headers: dict):
    """Test successful user creation."""
    user_data = {
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "newpass123",  # NOSONAR
        "first_name": "",
        "last_name": "",
        "is_active": True,
        "date_joined": datetime.utcnow().isoformat(),
    }
    response = await client.post(
        API_USERS_ENDPOINT, json=user_data, headers=superuser_token_headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]


@pytest.mark.asyncio
async def test_create_user_existing_email(
    client: AsyncClient, superuser_token_headers: dict, normal_user: User
):
    """Test creating user with existing email."""
    user_data = {
        "email": normal_user.email,
        "username": "different",
        "password": "newpass123",  # NOSONAR
        "first_name": "",
        "last_name": "",
        "is_active": True,
        "date_joined": datetime.utcnow().isoformat(),
    }
    response = await client.post(
        API_USERS_ENDPOINT, json=user_data, headers=superuser_token_headers
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_read_users(client: AsyncClient, superuser_token_headers: dict):
    """Test reading all users."""
    response = await client.get(API_USERS_ENDPOINT, headers=superuser_token_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) > 0


@pytest.mark.asyncio
async def test_read_user_by_id_not_found(
    client: AsyncClient, superuser_token_headers: dict
):
    """Test getting a non-existent user by ID."""
    response = await client.get("/api/v1/users/999", headers=superuser_token_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["code"] == ErrorCode.USER_DOES_NOT_EXIST_CODE


@pytest.mark.asyncio
async def test_read_users_normal_user(
    client: AsyncClient, normal_user_token_headers: dict
):
    """Test reading users as normal user."""
    response = await client.get(API_USERS_ENDPOINT, headers=normal_user_token_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    data = response.json()
    assert data["code"] == ErrorCode.NOT_SUPERUSER_CODE


@pytest.mark.asyncio
async def test_read_user_me(
    client: AsyncClient, normal_user: User, normal_user_token_headers: dict
):
    """Test reading current user info."""
    response = await client.get(API_ME_ENDPOINT, headers=normal_user_token_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == normal_user.email
    assert data["username"] == normal_user.username


@pytest.mark.asyncio
async def test_update_user_me(client: AsyncClient, normal_user_token_headers: dict):
    """Test updating current user info."""
    update_data = {"first_name": "Updated", "last_name": "Name"}
    response = await client.patch(
        API_ME_ENDPOINT, headers=normal_user_token_headers, json=update_data
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["first_name"] == update_data["first_name"]
    assert data["last_name"] == update_data["last_name"]


@pytest.mark.asyncio
async def test_delete_user(
    client: AsyncClient, superuser_token_headers: dict, normal_user: User
):
    """Test deleting a user."""
    response = await client.delete(
        f"/api/v1/users/{normal_user.id}", headers=superuser_token_headers
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
