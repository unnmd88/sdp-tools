from core.error_data import ErrorData
from core.exceptions import BaseAppError


class InfrastructureError(BaseAppError):
    code: str = ErrorData.INFRASTRUCTURE_ERROR.code
    message: str = ErrorData.INFRASTRUCTURE_ERROR.message
    http_status: int = ErrorData.INFRASTRUCTURE_ERROR.http_status_code


class RottenTokenError(InfrastructureError):
    code: str = ErrorData.TOKEN_ERROR.code
    message: str = ErrorData.TOKEN_ERROR.message
    http_status: int = ErrorData.TOKEN_ERROR.http_status_code


class InvalidTokenTypeError(InfrastructureError):
    code: str = ErrorData.BAD_REQUEST.code
    message: str = ErrorData.BAD_REQUEST.message
    http_status: int = ErrorData.BAD_REQUEST.http_status_code
