class ErrorCode:
    """Error code."""

    # General error
    INTERNAL_SERVER_ERROR_CODE = "E0000"
    INTERNAL_SERVER_ERROR_MESSAGE = "Internal server error."

    SERVICE_UNAVAILABLE_CODE = "E0001"
    SERVICE_UNAVAILABLE_MESSAGE = "Service unavailable."

    BAD_REQUEST_ERROR_CODE = "E0002"
    BAD_REQUEST_ERROR_MESSAGE = "Bad request."

    UNAUTHORIZED_ERROR_CODE = "E0003"
    UNAUTHORIZED_ERROR_MESSAGE = "Unauthorized error."

    FORBIDDEN_ERROR_CODE = "E0004"
    FORBIDDEN_ERROR_MESSAGE = "Forbidden error."

    NOT_FOUND_ERROR_CODE = "E0005"
    NOT_FOUND_ERROR_MESSAGE = "Not found error."

    VALIDATION_ERROR_CODE = "E0006"
    VALIDATION_ERROR_MESSAGE = "This field is invalid."

    RATE_LIMIT_EXCEEDED_CODE = "E0007"
    RATE_LIMIT_EXCEEDED_MESSAGE = "Rate limit exceeded."

    # Execute error
    EMAIL_ALREADY_EXISTS_CODE = "E0100"
    EMAIL_ALREADY_EXISTS_MESSAGE = "Email already exists."

    USERNAME_ALREADY_EXISTS_CODE = "E0101"
    USERNAME_ALREADY_EXISTS_MESSAGE = "Username already exists."

    USERNAME_OR_EMAIL_ALREADY_EXISTS_CODE = "E0101"
    USERNAME_OR_EMAIL_ALREADY_EXISTS_MESSAGE = "Username or email already exists."

    USERNAME_OR_PASSWORD_IS_INCORRECT_CODE = "E0102"  # noqa S105
    USERNAME_OR_PASSWORD_IS_INCORRECT_MESSAGE = "Username or password is incorrect."

    USER_DOES_NOT_EXIST_CODE = "E0103"
    USER_DOES_NOT_EXIST_MESSAGE = "User does not exist."

    USER_IS_INACTIVE_CODE = "E0104"
    USER_IS_INACTIVE_MESSAGE = "User is inactive"

    TOKEN_EXPIRED_CODE = "E0200"  # noqa S105
    TOKEN_EXPIRED_MESSAGE = "Token has expired."

    # Token errors
    INVALID_TOKEN_CODE = "E0201"
    INVALID_TOKEN_MESSAGE = "Invalid token."

    # User role errors
    NOT_SUPERUSER_CODE = "E0301"
    NOT_SUPERUSER_MESSAGE = "User is not a superuser."
