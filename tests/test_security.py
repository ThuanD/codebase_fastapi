from datetime import timedelta

import pytest
from jose import JWTError, jwt

from app.core.config import settings
from app.core.security import create_token, verify_token
from app.errors.exception import InvalidTokenError, TokenExpiredError


def test_create_access_token():
    """Test creating access token."""
    token = create_token("test-subject")
    decoded = jwt.decode(
        token,
        settings.SECRET_KEY.get_secret_value(),
        algorithms=[settings.SECURITY_ALGORITHM],
    )
    assert decoded["sub"] == "test-subject"
    assert decoded["type"] == "access"


def test_create_refresh_token():
    """Test creating refresh token."""
    token = create_token("test-subject", "refresh")
    decoded = jwt.decode(
        token,
        settings.SECRET_KEY.get_secret_value(),
        algorithms=[settings.SECURITY_ALGORITHM],
    )
    assert decoded["sub"] == "test-subject"
    assert decoded["type"] == "refresh"


def test_verify_token_success():
    """Test successful token verification."""
    token = create_token(123)
    subject = verify_token(token)
    assert subject == 123


def test_verify_token_expired():
    """Test expired token verification."""
    token = create_token("test-subject", expires_delta=timedelta(days=-1))
    try:
        verify_token(token)
        pytest.fail("Should have raised TokenExpiredError")
    except TokenExpiredError:
        pass


def test_verify_token_none():
    """Test invalid token verification."""
    token = create_token("")
    with pytest.raises(InvalidTokenError):
        verify_token(token)


def test_verify_token_invalid():
    """Test invalid token verification."""
    with pytest.raises(InvalidTokenError):
        verify_token("invalid-token")


def test_create_token_jwt_error(monkeypatch):
    """Test token creation with JWT encoding error."""

    def mock_encode(*args, **kwargs):
        raise JWTError("Encoding error")

    monkeypatch.setattr(jwt, "encode", mock_encode)
    with pytest.raises(InvalidTokenError):
        create_token("test-subject")


def test_verify_token_wrong_type():
    """Test token verification with wrong type."""
    token = create_token("test-subject", "refresh")
    with pytest.raises(InvalidTokenError):
        verify_token(token, "access")
