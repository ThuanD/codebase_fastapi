from datetime import UTC, datetime, timedelta
from typing import Optional, Union

from jose import JWTError, jwt

from app.core.config import settings
from app.core.constants import TokenType
from app.errors.exception import InvalidTokenError, TokenExpiredError


def create_token(
        subject: Union[int, str],
        token_type: str = TokenType.ACCESS_TOKEN,
        expires_delta: Optional[timedelta] = None,
) -> str:
    """Create JWT token.

    Args:
        subject: Subject to encode in token (usually user ID)
        token_type: Type of token ("access" or "refresh")
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT token as string

    Raises:
        InvalidTokenError: If token creation fails

    """
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + (
            timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS)
            if token_type == TokenType.ACCESS_TOKEN
            else timedelta(seconds=settings.REFRESH_TOKEN_EXPIRE_SECONDS)
        )

    to_encode = {"exp": expire, "sub": str(subject), "type": token_type}

    try:
        return jwt.encode(
            to_encode,
            settings.SECRET_KEY.get_secret_value(),
            algorithm=settings.SECURITY_ALGORITHM,
        )
    except JWTError as e:
        raise InvalidTokenError(message=str(e)) from e


def verify_token(
        token: str, token_type: str = TokenType.ACCESS_TOKEN) -> Union[int | str]:
    """Verify JWT token and return user ID.

    Args:
        token: JWT token to verify
        token_type: Type of token ("access" or "refresh")

    Returns:
        User ID if token is valid

    Raises:
        TokenExpiredError: If token has expired
        InvalidTokenError: If token is invalid

    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY.get_secret_value(),
            algorithms=[settings.SECURITY_ALGORITHM],
        )
        if payload.get("type") != token_type:
            raise InvalidTokenError("Invalid token type")

        user_id = payload.get("sub")
        if user_id is None:
            raise InvalidTokenError("Token missing user ID")

        return int(user_id)
    except jwt.ExpiredSignatureError as e:
        raise TokenExpiredError from e
    except JWTError as e:
        raise InvalidTokenError(message=str(e)) from e
