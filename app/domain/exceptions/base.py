"""
Модуль, содержащий базовые исключения.
"""

from core.error_data import ErrorData
from core.exceptions import BaseAppError

#
# class ApplicationError(Exception):
#     """Ошибка приложения."""


class DomainError(BaseAppError):
    """
    Базовое исключение домена.
    Все доменные исключения должны наследоваться от него.
    """

    code: str = ErrorData.DOMAIN_ERROR.code
    message: str = ErrorData.DOMAIN_ERROR.message
    http_status: int = ErrorData.DOMAIN_ERROR.http_status_code
