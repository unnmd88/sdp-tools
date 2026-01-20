from core.http_codes import HTTP_403_FORBIDDEN
from core.error_data import ErrorCodes
from domain.exceptions.base import DomainError


class DomainPermissionError(DomainError):
    """Ошибка прав доступа в домене."""

    code = ErrorCodes.PERMISSION_ERROR
    message = ErrorCodes.PERMISSION_ERROR
    http_status = HTTP_403_FORBIDDEN
