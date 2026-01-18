from core.http_codes import HTTP_404_NOT_FOUND
from core.error_codes import ErrorCodes
from domain.exceptions.base import DomainError


class DomainEntityNotFoundError (DomainError):
    """Класс исключения для ошибок, когда сущность не найдена. """

    code = ErrorCodes.ENTITY_NOT_FOUND
    message = ErrorCodes.ENTITY_NOT_FOUND
    http_status = HTTP_404_NOT_FOUND



