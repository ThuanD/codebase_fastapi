from datetime import timedelta

from fastapi import status
from fastapi.testclient import TestClient

from app.core.security import create_token
from app.errors.error_code import ErrorCode
from app.models.user import User


def test_login(client: TestClient, normal_user: User):
    """Test successful login."""
    login_data = {"username": normal_user.email, "password": "testpass123"}
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == status.HTTP_200_OK
    tokens = response.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens


def test_refresh_token(client: TestClient, normal_user: User):
    """Test successful token refresh."""
    refresh_token = create_token(str(normal_user.id), "refresh")
    response = client.post(
        "/api/v1/auth/refresh", json={"refresh_token": refresh_token}
    )
    assert response.status_code == status.HTTP_200_OK
    tokens = response.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens


def test_get_me(client: TestClient, normal_user: User, normal_user_token_headers: dict):
    """Test getting current user info."""
    response = client.get("/api/v1/auth/me", headers=normal_user_token_headers)
    assert response.status_code == status.HTTP_200_OK
    user_data = response.json()
    assert user_data["email"] == normal_user.email
    assert user_data["username"] == normal_user.username


def test_login_wrong_password(client: TestClient, normal_user: User):
    """Test login with wrong password."""
    login_data = {"username": normal_user.email, "password": "wrongpass"}
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_inactive_user(client: TestClient, inactive_user: User):
    """Test login with inactive user."""
    login_data = {"username": inactive_user.email, "password": "inactive123"}
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_refresh_token_success(client: TestClient, normal_user: User):
    """Test successful token refresh."""
    refresh_token = create_token(str(normal_user.id), "refresh")
    response = client.post(
        "/api/v1/auth/refresh", json={"refresh_token": refresh_token}
    )
    assert response.status_code == status.HTTP_200_OK
    tokens = response.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens


def test_refresh_token_expired(client: TestClient, normal_user: User):
    """Test refresh with expired token."""
    expired_token = create_token(
        str(normal_user.id), "refresh", expires_delta=timedelta(days=-10)
    )
    response = client.post(
        "/api/v1/auth/refresh", json={"refresh_token": expired_token}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert data["code"] == ErrorCode.TOKEN_EXPIRED_CODE
