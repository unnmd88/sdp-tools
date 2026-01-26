from core.error_data import ErrorData
from core.exceptions import BaseAppError


class ServiceError(BaseAppError):
    code: str = ErrorData.APPLICATION_ERROR.code
    message: str = ErrorData.APPLICATION_ERROR.message
    http_status: int = ErrorData.APPLICATION_ERROR.http_status_code


class UnauthorizedError(BaseAppError):
    code: str = ErrorData.UNAUTHORIZED.code
    message: str = ErrorData.UNAUTHORIZED.message
    http_status: int = ErrorData.UNAUTHORIZED.http_status_code


class ForbiddenError(BaseAppError):
    code: str = ErrorData.FORBIDDEN.code
    message: str = ErrorData.FORBIDDEN.message
    http_status: int = ErrorData.FORBIDDEN.http_status_code
