from core.error_data import ErrorData
from core.exceptions import BaseAppError


class InfrastructureError(BaseAppError):
    """
    Базовое исключение инфраструктуры.
    Все инфраструктурные исключения должны наследоваться от него.
    """

    DEFAULT_CODE = ErrorData.INFRASTRUCTURE_ERROR.code
    DEFAULT_MESSAGE = ErrorData.INFRASTRUCTURE_ERROR.message


class TokenError(InfrastructureError):
    DEFAULT_CODE = ErrorData.TOKEN_ERROR.code
    DEFAULT_MESSAGE = ErrorData.TOKEN_ERROR.message


class RottenTokenError(TokenError):
    DEFAULT_CODE = ErrorData.ROTTEN_TOKEN_ERROR.code
    DEFAULT_MESSAGE = ErrorData.ROTTEN_TOKEN_ERROR.message


class InvalidTokenTypeError(TokenError):
    DEFAULT_CODE = ErrorData.INVALID_TOKEN_TYPE.code
    DEFAULT_MESSAGE = ErrorData.INVALID_TOKEN_TYPE.message
