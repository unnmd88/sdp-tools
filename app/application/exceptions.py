from core.error_codes import ErrorCodes
from core.exceptions import BaseAppError


class ApplicationLayerError(BaseAppError):
    """
    Базовое исключение слой приложения.
    Все исключения слоя приложения должны наследоваться от него.
    """

    DEFAULT_CODE = ErrorCodes.APPLICATION_ERROR.code
    DEFAULT_PRIVATE_MESSAGE = ErrorCodes.APPLICATION_ERROR.private_message
    DEFAULT_PUBLIC_MESSAGE = ErrorCodes.APPLICATION_ERROR.public_message


class AuthenticationError(ApplicationLayerError):
    DEFAULT_CODE = ErrorCodes.AUTHENTICATION_FAILED.code
    DEFAULT_PRIVATE_MESSAGE = ErrorCodes.AUTHENTICATION_FAILED.private_message
    DEFAULT_PUBLIC_MESSAGE = ErrorCodes.AUTHENTICATION_FAILED.public_message


class InactiveAccountError(ApplicationLayerError):
    DEFAULT_CODE = ErrorCodes.INACTIVE_ACCOUNT.code
    DEFAULT_PRIVATE_MESSAGE = ErrorCodes.INACTIVE_ACCOUNT.private_message
    DEFAULT_PUBLIC_MESSAGE = ErrorCodes.INACTIVE_ACCOUNT.public_message


class PermissionDeniedError(ApplicationLayerError):
    DEFAULT_CODE = ErrorCodes.FORBIDDEN.code
    DEFAULT_PRIVATE_MESSAGE = ErrorCodes.FORBIDDEN.private_message
    DEFAULT_PUBLIC_MESSAGE = ErrorCodes.FORBIDDEN.public_message