from fastapi import status
from fastapi.testclient import TestClient

from app.errors.error_code import ErrorCode
from app.models.user import User


def test_create_user(client: TestClient, superuser_token_headers: dict):
    """Test creating a new user."""
    response = client.post(
        "/api/v1/users",
        headers=superuser_token_headers,
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass123",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"


def test_get_user(client: TestClient, superuser_token_headers: dict, normal_user: User):
    """Test getting a specific user."""
    response = client.get(
        f"/api/v1/users/{normal_user.id}", headers=superuser_token_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == normal_user.email
    assert data["username"] == normal_user.username


def test_create_user_success(client, superuser_token_headers):
    """Test successful user creation by superuser."""
    user_data = {
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "newpass123",
    }
    response = client.post(
        "/api/v1/users", json=user_data, headers=superuser_token_headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]


def test_create_user_existing_email(client, superuser_token_headers, normal_user):
    """Test user creation with existing email."""
    user_data = {
        "email": "user@example.com",  # Already exists
        "username": "different",
        "password": "newpass123",
    }
    response = client.post(
        "/api/v1/users", json=user_data, headers=superuser_token_headers
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_read_users(client: TestClient, superuser_token_headers: dict):
    """Test reading all users."""
    response = client.get("/api/v1/users", headers=superuser_token_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) > 0


def test_read_users_normal_user(client: TestClient, normal_user_token_headers: dict):
    """Test reading all users as normal user (should fail)."""
    response = client.get("/api/v1/users", headers=normal_user_token_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    data = response.json()
    assert data["code"] == ErrorCode.NOT_SUPERUSER_CODE


def test_read_user_me(
    client: TestClient, normal_user: User, normal_user_token_headers: dict
):
    """Test reading own user information."""
    response = client.get("/api/v1/users/me", headers=normal_user_token_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == normal_user.email
    assert data["username"] == normal_user.username


def test_update_user_me(client: TestClient, normal_user_token_headers: dict):
    """Test updating own user information."""
    update_data = {"first_name": "Updated", "last_name": "Name"}
    response = client.patch(
        "/api/v1/users/me", headers=normal_user_token_headers, json=update_data
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["first_name"] == update_data["first_name"]
    assert data["last_name"] == update_data["last_name"]


def test_delete_user(
    client: TestClient, superuser_token_headers: dict, normal_user: User
):
    """Test deleting a user."""
    response = client.delete(
        f"/api/v1/users/{normal_user.id}", headers=superuser_token_headers
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
