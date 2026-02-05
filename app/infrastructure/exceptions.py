from core.error_codes import ErrorCodes
from core.exceptions import BaseAppError


class InfrastructureError(BaseAppError):
    """
    Базовое исключение инфраструктуры.
    Все инфраструктурные исключения должны наследоваться от него.
    """

    DEFAULT_CODE = ErrorCodes.INFRASTRUCTURE_ERROR.code
    DEFAULT_PRIVATE_MESSAGE = ErrorCodes.INFRASTRUCTURE_ERROR.private_message
    DEFAULT_PUBLIC_MESSAGE = ErrorCodes.INFRASTRUCTURE_ERROR.public_message


class RepositoryError(InfrastructureError):
    """ Базовое исключение репозитория. """

    DEFAULT_CODE = ErrorCodes.REPOSITORY_ERROR.code
    DEFAULT_PRIVATE_MESSAGE = ErrorCodes.REPOSITORY_ERROR.private_message
    DEFAULT_PUBLIC_MESSAGE = ErrorCodes.REPOSITORY_ERROR.public_message


class RepositoryConnectionError(RepositoryError):
    DEFAULT_CODE = ErrorCodes.REPOSITORY_CONNECTION_ERROR.code
    DEFAULT_PRIVATE_MESSAGE = ErrorCodes.REPOSITORY_CONNECTION_ERROR.private_message
    DEFAULT_PUBLIC_MESSAGE = ErrorCodes.REPOSITORY_CONNECTION_ERROR.public_message


class RepositoryIntegrityError(RepositoryError):
    DEFAULT_CODE = ErrorCodes.REPOSITORY_INTEGRITY_ERROR.code
    DEFAULT_PRIVATE_MESSAGE = ErrorCodes.REPOSITORY_INTEGRITY_ERROR.private_message
    DEFAULT_PUBLIC_MESSAGE = ErrorCodes.REPOSITORY_INTEGRITY_ERROR.public_message


class RepositoryUpdateError(RepositoryError):

    DEFAULT_CODE = ErrorCodes.REPOSITORY_UPDATE_ERROR.code
    DEFAULT_PRIVATE_MESSAGE = ErrorCodes.REPOSITORY_UPDATE_ERROR.private_message
    DEFAULT_PUBLIC_MESSAGE = ErrorCodes.REPOSITORY_UPDATE_ERROR.public_message


class RepositoryCorruptedError(RepositoryError):

    DEFAULT_CODE = ErrorCodes.CORRUPTED_DATA_ERROR.code
    DEFAULT_PRIVATE_MESSAGE = ErrorCodes.CORRUPTED_DATA_ERROR.private_message
    DEFAULT_PUBLIC_MESSAGE = ErrorCodes.CORRUPTED_DATA_ERROR.public_message


class TokenError(InfrastructureError):
    DEFAULT_CODE = ErrorCodes.TOKEN_ERROR.code
    DEFAULT_PRIVATE_MESSAGE = ErrorCodes.TOKEN_ERROR.private_message
    DEFAULT_PUBLIC_MESSAGE = ErrorCodes.TOKEN_ERROR.public_message


class TokenExpiredError(TokenError):
    DEFAULT_CODE = ErrorCodes.TOKEN_EXPIRED_ERROR.code
    DEFAULT_PRIVATE_MESSAGE = ErrorCodes.TOKEN_EXPIRED_ERROR.private_message
    DEFAULT_PUBLIC_MESSAGE = ErrorCodes.TOKEN_EXPIRED_ERROR.public_message


class InvalidTokenTypeError(TokenError):
    DEFAULT_CODE = ErrorCodes.INVALID_TOKEN_TYPE.code
    DEFAULT_PRIVATE_MESSAGE = ErrorCodes.INVALID_TOKEN_TYPE.private_message
    DEFAULT_PUBLIC_MESSAGE = ErrorCodes.INVALID_TOKEN_TYPE.public_message
