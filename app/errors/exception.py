from typing import Any, Dict, Optional

from app.errors.error_code import ErrorCode


class BaseError(Exception):
    """Base class for all application errors."""

    def __init__(
        self,
        message: Optional[str] = None,
        code: Optional[str] = None,
        status_code: Optional[int] = None,
    ) -> None:
        """Initialize error.

        Args:
            message: Error message
            code: Error code
            status_code: HTTP status code

        """
        self.message = message or self.message
        self.code = code or self.code
        self.status_code = status_code or self.status_code
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary.

        Returns:
            Dictionary representation of error

        """
        return {
            "code": self.code,
            "message": self.message,
            "status_code": self.status_code,
        }


class NotFoundError(BaseError):
    """Resource not found error."""

    status_code = 404
    code = ErrorCode.NOT_FOUND_ERROR_CODE
    message = ErrorCode.NOT_FOUND_ERROR_MESSAGE


class ValidationError(BaseError):
    """Validation error."""

    status_code = 422
    code = ErrorCode.VALIDATION_ERROR_CODE
    message = ErrorCode.VALIDATION_ERROR_MESSAGE


class UnauthorizedError(BaseError):
    """Unauthorized error."""

    status_code = 401
    code = ErrorCode.UNAUTHORIZED_ERROR_CODE
    message = ErrorCode.UNAUTHORIZED_ERROR_MESSAGE


class ForbiddenError(BaseError):
    """Forbidden error."""

    status_code = 403
    code = ErrorCode.FORBIDDEN_ERROR_CODE
    message = ErrorCode.FORBIDDEN_ERROR_MESSAGE


class TokenExpiredError(BaseError):
    """Token expired error."""

    status_code = 401
    code = ErrorCode.TOKEN_EXPIRED_CODE
    message = ErrorCode.TOKEN_EXPIRED_MESSAGE


class InvalidTokenError(BaseError):
    """Invalid token error."""

    status_code = 401
    code = ErrorCode.INVALID_TOKEN_CODE
    message = ErrorCode.INVALID_TOKEN_MESSAGE


class UserNotFoundError(BaseError):
    """User not found error."""

    status_code = 404
    code = ErrorCode.USER_DOES_NOT_EXIST_CODE
    message = ErrorCode.USER_DOES_NOT_EXIST_MESSAGE


class UserIsInactiveError(BaseError):
    """User is inactive error."""

    status_code = 401
    code = ErrorCode.USER_IS_INACTIVE_CODE
    message = ErrorCode.USER_IS_INACTIVE_MESSAGE


class UsernameOrEmailAlreadyExistError(BaseError):
    """Username or email already exists error."""

    status_code = 422
    code = ErrorCode.USERNAME_OR_EMAIL_ALREADY_EXISTS_CODE
    message = ErrorCode.USERNAME_OR_EMAIL_ALREADY_EXISTS_MESSAGE


class UsernameOrPasswordIsIncorrectError(BaseError):
    """Username or password is incorrect error."""

    status_code = 401
    code = ErrorCode.USERNAME_OR_PASSWORD_IS_INCORRECT_CODE
    message = ErrorCode.USERNAME_OR_PASSWORD_IS_INCORRECT_MESSAGE


class NotSuperuserError(BaseError):
    """Not superuser error."""

    status_code = 403
    code = ErrorCode.NOT_SUPERUSER_CODE
    message = ErrorCode.NOT_SUPERUSER_MESSAGE


class InternalServerError(BaseError):
    """Internal server error."""

    code = ErrorCode.INTERNAL_SERVER_ERROR_CODE
    message = ErrorCode.INTERNAL_SERVER_ERROR_MESSAGE
    status_code = 500


class ServiceUnavailableError(BaseError):
    """Service Unavailable error."""

    code = ErrorCode.SERVICE_UNAVAILABLE_CODE
    message = ErrorCode.SERVICE_UNAVAILABLE_MESSAGE
    status_code = 503


class BadRequestError(BaseError):
    """Bad Request error."""

    status_code = 400
    code = ErrorCode.BAD_REQUEST_ERROR_CODE
    message = ErrorCode.BAD_REQUEST_ERROR_MESSAGE


class UsernameAlreadyExistError(BaseError):
    """Username already exist error."""

    status_code = 422
    code = ErrorCode.USERNAME_ALREADY_EXISTS_CODE
    message = ErrorCode.USERNAME_ALREADY_EXISTS_MESSAGE


class EmailAlreadyExistError(BaseError):
    """Email already exist error."""

    status_code = 422
    code = ErrorCode.EMAIL_ALREADY_EXISTS_CODE
    message = ErrorCode.EMAIL_ALREADY_EXISTS_MESSAGE


class RateLimitExceededError(BaseError):
    """Rate Limit Exceeded error."""

    code = ErrorCode.RATE_LIMIT_EXCEEDED_CODE
    message = ErrorCode.RATE_LIMIT_EXCEEDED_MESSAGE
    status_code = 429


class UserDoesNotExistError(BaseError):
    """User does not exist error."""

    status_code = 404
    code = ErrorCode.USER_DOES_NOT_EXIST_CODE
    message = ErrorCode.USER_DOES_NOT_EXIST_MESSAGE
