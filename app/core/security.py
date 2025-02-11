from calendar import timegm
from datetime import UTC, datetime, timedelta
from typing import Any, Optional, Union

from jose import jwt
from pydantic import ValidationError

from app.core.config import settings
from app.errors.exception import InvalidTokenError, TokenExpiredError


def create_token(
    subject: Union[str, Any],
    token_type: str = "access",
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create JWT token.

    Args:
        subject: Subject to encode in token (usually user ID)
        token_type: Type of token ("access" or "refresh")
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT token as string

    """
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        if token_type == "access":
            expire = datetime.now() + timedelta(
                seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS
            )
        else:  # refresh token
            expire = datetime.now() + timedelta(
                seconds=settings.REFRESH_TOKEN_EXPIRE_SECONDS
            )

    to_encode = {"exp": expire, "sub": str(subject), "type": token_type}

    try:
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY.get_secret_value(),
            algorithm=settings.SECURITY_ALGORITHM,
        )
        return encoded_jwt
    except jwt.JWTError as e:
        raise InvalidTokenError(message=str(e))


def verify_token(token: str, token_type: str = "access") -> Optional[str]:
    """Verify JWT token.

    Args:
        token: Token to verify
        token_type: Expected token type ("access" or "refresh")

    Returns:
        Subject from token if valid, None otherwise

    Raises:
        TokenExpiredError: If token has expired
        InvalidTokenError: If token is invalid

    """
    try:
        decoded_token = jwt.decode(
            token,
            settings.SECRET_KEY.get_secret_value(),
            algorithms=[settings.SECURITY_ALGORITHM],
        )
        # Check token type first
        if decoded_token["type"] != token_type:
            raise InvalidTokenError(
                message=f"Invalid token type. Expected {token_type}"
            )
        # Check expiration
        if "exp" in decoded_token:
            now = timegm(datetime.now(UTC).utctimetuple())
            if decoded_token["exp"] <= now:
                raise TokenExpiredError()

        return decoded_token["sub"]
    except jwt.ExpiredSignatureError:
        raise TokenExpiredError()
    except (jwt.JWTError, ValidationError) as e:
        raise InvalidTokenError(message=str(e))
