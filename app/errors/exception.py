from app.errors.error_code import ErrorCode


class BaseError(Exception):
    """Base error class."""

    code = "error"
    message = "A server error occurred."
    status_code = 500

    def __init__(
        self, code: int = None, message: str | object = None, status_code: int = None
    ) -> None:
        """Initialize the exception."""
        super().__init__()
        if code:
            self.code = code
        if message:
            self.message = message
        if status_code:
            self.status_code = status_code

    def to_dict(self) -> dict:
        """Return a dictionary representation of the error."""
        return {"code": self.code, "message": self.message}


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


class NotFoundError(BaseError):
    """Not Found error."""

    status_code = 404
    code = ErrorCode.NOT_FOUND_ERROR_CODE
    message = ErrorCode.NOT_FOUND_ERROR_MESSAGE


class RequestBodyValidationError(BaseError):
    """Request body validation error."""

    status_code = 422
    code = ErrorCode.VALIDATION_ERROR_CODE
    message = ErrorCode.VALIDATION_ERROR_MESSAGE


class RateLimitExceededError(BaseError):
    """Rate Limit Exceeded error."""

    code = ErrorCode.RATE_LIMIT_EXCEEDED_CODE
    message = ErrorCode.RATE_LIMIT_EXCEEDED_MESSAGE
    status_code = 429


class TokenExpiredError(BaseError):
    """Token expired error."""

    status_code = 401
    code = ErrorCode.TOKEN_EXPIRED_CODE
    message = ErrorCode.TOKEN_EXPIRED_MESSAGE


class UserDoesNotExistError(BaseError):
    """User does not exist error."""

    status_code = 404
    code = ErrorCode.USER_DOES_NOT_EXIST_CODE
    message = ErrorCode.USER_DOES_NOT_EXIST_MESSAGE


class UserIsInactiveError(BaseError):
    """User is inactive error."""

    status_code = 400
    code = ErrorCode.USER_IS_INACTIVE_CODE
    message = ErrorCode.USER_IS_INACTIVE_MESSAGE


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


class UsernameOrEmailAlreadyExistError(BaseError):
    """Username or email already exist error."""

    status_code = 422
    code = ErrorCode.USERNAME_OR_EMAIL_ALREADY_EXISTS_CODE
    message = ErrorCode.USERNAME_OR_EMAIL_ALREADY_EXISTS_MESSAGE


class UsernameOrPasswordIsIncorrectError(BaseError):
    """Username or password is incorrect error."""

    status_code = 401
    code = ErrorCode.USERNAME_OR_PASSWORD_IS_INCORRECT_CODE
    message = ErrorCode.USERNAME_OR_PASSWORD_IS_INCORRECT_MESSAGE


class InvalidTokenError(BaseError):
    """Invalid token error."""

    status_code = 401
    code = ErrorCode.INVALID_TOKEN_CODE
    message = ErrorCode.INVALID_TOKEN_MESSAGE


class NotSuperuserError(BaseError):
    """User is not superuser error."""

    status_code = 403
    code = ErrorCode.NOT_SUPERUSER_CODE
    message = ErrorCode.NOT_SUPERUSER_MESSAGE
