"""
Модуль, содержащий базовые исключения.
"""


class ApplicationError(Exception):
    """Ошибка приложения."""


class DomainValidationError(ApplicationError):
    """Ошибка валидации доменной сущности."""
