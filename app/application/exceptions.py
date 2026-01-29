from core.error_data import ErrorData
from core.exceptions import BaseAppError


class ApplicationLayerError(BaseAppError):
    """
    Базовое исключение слой приложения.
    Все исключения слоя приложения должны наследоваться от него.
    """

    DEFAULT_CODE = ErrorData.APPLICATION_ERROR.code
    DEFAULT_MESSAGE = ErrorData.APPLICATION_ERROR.message


class NotFoundError(ApplicationLayerError):

    DEFAULT_CODE = ErrorData.NOT_FOUND.code
    DEFAULT_MESSAGE = ErrorData.NOT_FOUND.message


class AuthenticationError(ApplicationLayerError):

    DEFAULT_CODE = ErrorData.UNAUTHORIZED.code
    DEFAULT_MESSAGE = ErrorData.UNAUTHORIZED.message


class InactiveAccountError(ApplicationLayerError):

    DEFAULT_CODE = ErrorData.INACTIVE_ACCOUNT.code
    DEFAULT_MESSAGE = ErrorData.INACTIVE_ACCOUNT.message
