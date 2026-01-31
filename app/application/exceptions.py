from core.error_codes import ErrorCodes
from core.exceptions import BaseAppError


class ApplicationLayerError(BaseAppError):
    """
    Базовое исключение слой приложения.
    Все исключения слоя приложения должны наследоваться от него.
    """

    DEFAULT_CODE = ErrorCodes.APPLICATION_ERROR.code
    DEFAULT_MESSAGE = ErrorCodes.APPLICATION_ERROR.message


class NotFoundError(ApplicationLayerError):
    DEFAULT_CODE = ErrorCodes.NOT_FOUND.code
    DEFAULT_MESSAGE = ErrorCodes.NOT_FOUND.message


class AuthenticationError(ApplicationLayerError):
    DEFAULT_CODE = ErrorCodes.UNAUTHORIZED.code
    DEFAULT_MESSAGE = ErrorCodes.UNAUTHORIZED.message


class InactiveAccountError(ApplicationLayerError):
    DEFAULT_CODE = ErrorCodes.INACTIVE_ACCOUNT.code
    DEFAULT_MESSAGE = ErrorCodes.INACTIVE_ACCOUNT.message
