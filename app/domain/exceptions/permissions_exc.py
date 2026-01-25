from core.error_data import ErrorData
from domain.exceptions.base import DomainError


class DomainInactiveUserError(DomainError):
    """Ошибка прав доступа в домене."""

    code = ErrorData.ACCOUNT_LOCKED.code
    message = ErrorData.ACCOUNT_LOCKED.message
    http_status = ErrorData.ACCOUNT_LOCKED.http_status_code
