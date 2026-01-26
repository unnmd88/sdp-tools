"""
Модуль, содержащий базовые исключения.
"""

from core.exceptions import BaseAppError


class DomainError(BaseAppError):
    """
    Базовое исключение домена.
    Все доменные исключения должны наследоваться от него.
    """

    DEFAULT_CODE = "DOMAIN_ERROR"
    DEFAULT_MESSAGE = "Ошибка домена"
