from core.exceptions.base import ApplicationError


class NotFoundError(ApplicationError):
    """Ошибка, возникающая если объект не найден."""


class CreateError(ApplicationError):
    """Ошибка создания нового объекта."""


class CreateErrorAlreadyExists(ApplicationError):
    """Ошибка создания нового объекта по причине, что такой уже существует."""


class UpdateError(ApplicationError):
    """Ошибка обновления существующего объекта."""


class DeleteError(ApplicationError):
    """Ошибка удаления существующего объекта."""
