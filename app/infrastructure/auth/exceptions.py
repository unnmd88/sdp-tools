from core.error_codes import ErrorCodes
from core.exceptions import BaseAppError


class InfrastructureError(BaseAppError):
    code: str = ErrorCodes.INFRASTRUCTURE_ERROR.code
    message: str = ErrorCodes.INFRASTRUCTURE_ERROR.message


class RottenTokenError(InfrastructureError):
    code: str = ErrorCodes.TOKEN_ERROR.code
    message: str = ErrorCodes.TOKEN_ERROR.message


class InvalidTokenTypeError(InfrastructureError):
    code: str = ErrorCodes.BAD_REQUEST.code
    message: str = ErrorCodes.BAD_REQUEST.message
