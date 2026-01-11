"""
Модуль, содержащий базовые исключения.
"""


class ApplicationError(Exception):
    """Ошибка приложения."""


class DomainValidationError(ApplicationError):
    """Ошибка валидации доменной сущности."""


class DomainTypeValidationError(DomainValidationError):
    """Ошибка валидации типа данных доменной сущности."""

    def __init__(
        self,
        *,
        arg_name: str,
        expected: str,
    ):
        self._detail = f'Неверный тип данных для {arg_name!r}. Ожидается {expected!r}.'
        super().__init__(self._detail)

    @property
    def detail(self):
        return self._detail


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


class UserPermissionsError(ApplicationError):
    """Ошибка доступа к данным и сервисам в связи с отсутствием прав пользователя."""

    def __init__(self, type_permission: str = ''):
        self.detail = f'Доступ {type_permission} запрещён'.replace("  ", "")
        super().__init__(self.detail)



