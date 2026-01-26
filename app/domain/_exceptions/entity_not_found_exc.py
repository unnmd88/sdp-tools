from core.error_data import ErrorData
from domain._exceptions.base import DomainError


class DomainEntityNotFoundError(DomainError):
    """Класс исключения для ошибок, когда сущность не найдена."""

    code = ErrorData.ENTITY_NOT_FOUND.code
    message = ErrorData.ENTITY_NOT_FOUND.message
    http_status = ErrorData.ENTITY_NOT_FOUND.http_status_code
