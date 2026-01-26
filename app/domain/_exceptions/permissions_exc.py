from core.error_data import ErrorData
from domain._exceptions.base import DomainError


class DomainUnauthorizedError(DomainError):
    code = ErrorData.UNAUTHORIZED.code
    message = ErrorData.UNAUTHORIZED.message
    http_status = ErrorData.UNAUTHORIZED.http_status_code


class DomainInactiveUserError(DomainError):
    """Ошибка прав доступа в домене."""

    code = ErrorData.ACCOUNT_LOCKED.code
    message = ErrorData.ACCOUNT_LOCKED.message
    http_status = ErrorData.ACCOUNT_LOCKED.http_status_code


class DomainUserPermissionError(DomainError):
    """Ошибка прав доступа в домене."""

    code = ErrorData.FORBIDDEN.code
    message = ErrorData.FORBIDDEN.message
    http_status = ErrorData.FORBIDDEN.http_status_code
