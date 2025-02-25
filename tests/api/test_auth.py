from datetime import timedelta

from fastapi import status

import pytest
from httpx import AsyncClient

from app.core.security import create_token
from app.errors.error_code import ErrorCode
from app.models.user import User


@pytest.mark.asyncio
async def test_register(client: AsyncClient):
    """Test user registration."""
    register_data = {
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "newpass123",
        "first_name": "New",
        "last_name": "User",
    }
    response = await client.post("/api/v1/auth/register", json=register_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == register_data["email"]
    assert data["username"] == register_data["username"]


@pytest.mark.asyncio
async def test_register_invalid_username(client: AsyncClient):
    """Test registration with non-alphanumeric username."""
    register_data = {
        "email": "newuser2@example.com",
        "username": "new user!",  # Không alphanumeric
        "password": "newpass123",
        "first_name": "New",
        "last_name": "User",
    }
    response = await client.post("/api/v1/auth/register", json=register_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_login(client: AsyncClient, normal_user: User):
    """Test successful login."""
    login_data = {"email": normal_user.email, "password": "testpass123"}
    response = await client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == status.HTTP_200_OK
    tokens = response.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens


@pytest.mark.asyncio
async def test_logout(client: AsyncClient, normal_user_token_headers: dict):
    """Test user logout."""
    response = await client.post("/api/v1/auth/logout",
                                 headers=normal_user_token_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["message"] == "Successfully logged out"


@pytest.mark.asyncio
async def test_get_me(
        client: AsyncClient, normal_user: User, normal_user_token_headers: dict
):
    """Test getting current user info."""
    response = await client.get("/api/v1/auth/me", headers=normal_user_token_headers)
    assert response.status_code == status.HTTP_200_OK
    user_data = response.json()
    assert user_data["email"] == normal_user.email
    assert user_data["username"] == normal_user.username


@pytest.mark.asyncio
async def test_get_me_invalid_token(client: AsyncClient):
    """Test getting user info with invalid token."""
    headers = {"Authorization": "Bearer invalid_token"}
    response = await client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert data["code"] == ErrorCode.INVALID_TOKEN_CODE


@pytest.mark.asyncio
async def test_get_me_expired_token(client: AsyncClient, normal_user: User):
    """Test getting user info with expired token."""
    expired_token = create_token(str(normal_user.id), "access",
                                 expires_delta=timedelta(days=-1))
    headers = {"Authorization": f"Bearer {expired_token}"}
    response = await client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert data["code"] == ErrorCode.TOKEN_EXPIRED_CODE


@pytest.mark.asyncio
async def test_get_me_inactive_user(client: AsyncClient, inactive_user: User):
    """Test getting user info with inactive user."""
    headers = {"Authorization": f"Bearer {create_token(str(inactive_user.id))}"}
    response = await client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert data["code"] == ErrorCode.USER_IS_INACTIVE_CODE


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, normal_user: User):
    """Test login with wrong password."""
    login_data = {"email": normal_user.email, "password": "wrongpass"}
    response = await client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_login_inactive_user(client: AsyncClient, inactive_user: User):
    """Test login with inactive user."""
    login_data = {"email": inactive_user.email, "password": "inactive123"}
    response = await client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_refresh_token_success(client: AsyncClient, normal_user: User):
    """Test successful token refresh."""
    refresh_token = create_token(str(normal_user.id), "refresh")
    response = await client.post(
        "/api/v1/auth/refresh", json={"refresh_token": refresh_token}
    )
    assert response.status_code == status.HTTP_200_OK
    tokens = response.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens


@pytest.mark.asyncio
async def test_refresh_token_expired(client: AsyncClient, normal_user: User):
    """Test refresh with expired token."""
    expired_token = create_token(
        str(normal_user.id), "refresh", expires_delta=timedelta(days=-10)
    )
    response = await client.post(
        "/api/v1/auth/refresh", json={"refresh_token": expired_token}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert data["code"] == ErrorCode.TOKEN_EXPIRED_CODE
