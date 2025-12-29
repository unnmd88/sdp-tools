"""
Модуль, содержащий базовые исключения.
"""


class ApplicationError(Exception):
    """Ошибка приложения."""


class NotFoundError(ApplicationError):
    """Ошибка поиска объекта."""


class CreateError(ApplicationError):
    """Ошибка создания нового объекта."""


class CreateErrorAlreadyExists(ApplicationError):
    """Ошибка создания нового объекта по причине, что такой уже существует. """


class UpdateError(ApplicationError):
    """Ошибка обновления существующего объекта."""


class DeleteError(ApplicationError):
    """Ошибка удаления существующего объекта."""


class PermissionsError(ApplicationError):
    """Ошибка доступа к данным и сервисам в связи с отсутствием прав."""