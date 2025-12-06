"""
Модуль, содержащий базовые исключения.
"""


class ApplicationException(Exception):
    """Ошибка приложения."""


class NotFoundException(ApplicationException):
    """Ошибка поиска объекта."""


class CreateException(ApplicationException):
    """Ошибка создания нового объекта."""


class UpdateException(ApplicationException):
    """Ошибка обновления существующего объекта."""
