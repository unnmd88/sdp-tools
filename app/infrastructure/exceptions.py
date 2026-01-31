from core.error_codes import ErrorCodes
from core.exceptions import BaseAppError


class InfrastructureError(BaseAppError):
    """
    Базовое исключение инфраструктуры.
    Все инфраструктурные исключения должны наследоваться от него.
    """

    DEFAULT_CODE = ErrorCodes.INFRASTRUCTURE_ERROR.code
    DEFAULT_MESSAGE = ErrorCodes.INFRASTRUCTURE_ERROR.message


class TokenError(InfrastructureError):
    DEFAULT_CODE = ErrorCodes.TOKEN_ERROR.code
    DEFAULT_MESSAGE = ErrorCodes.TOKEN_ERROR.message


class RottenTokenError(TokenError):
    DEFAULT_CODE = ErrorCodes.ROTTEN_TOKEN_ERROR.code
    DEFAULT_MESSAGE = ErrorCodes.ROTTEN_TOKEN_ERROR.message


class InvalidTokenTypeError(TokenError):
    DEFAULT_CODE = ErrorCodes.INVALID_TOKEN_TYPE.code
    DEFAULT_MESSAGE = ErrorCodes.INVALID_TOKEN_TYPE.message
