from core.http_codes import HTTP_409_CONFLICT
from core.error_codes import ErrorCodes
from domain.exceptions.base import DomainError


class DomainConflictError(DomainError):
    """Конфликт данных (дублирование, одновременное изменение)."""

    code = ErrorCodes.CONFLICT_ERROR
    message = ErrorCodes.CONFLICT_ERROR
    http_status = HTTP_409_CONFLICT