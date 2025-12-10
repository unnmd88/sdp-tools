"""
Модуль, содержащий уточняющие исключения.
"""

from core.exceptions.base import (
    ApplicationError,
    NotFoundError,
    CreateError, UpdateError, PermissionsError,
)

INVALID_DESCRIPTION_EXCEPTION_TEXT = (
    'Поле description не должно превышать 255 символов.'
)


class DomainValidationError(ApplicationError):
    """Ошибка валидации доменной сущности."""

    @property
    def detail(self):
        return f'Ошибка валидации. {". ".join(self.args)}'


class UserInactiveError(ApplicationError):
    """Неактивный пользователь пытается осуществлять какие-либо действия. """


class UserNotFoundException(NotFoundError):
    """Ошибка поиска user."""

    @property
    def detail(self):
        return f'Пользователь не найден.'


class UserNotFoundByIdException(UserNotFoundException):
    """Ошибка поиска user по id."""

    def __init__(
        self,
        user_id: int,
    ):
        self._id = user_id
        super().__init__(self.detail)

    @property
    def detail(self):
        return f'Пользователь с id={self._id!r} не найден.'


class UserNotFoundByUsernameException(UserNotFoundException):
    """Ошибка поиска user по username."""

    def __init__(
        self,
        username: str,
    ):
        self._id = username
        super().__init__(self.detail)

    @property
    def detail(self):
        return f'Пользователь с username={self._id!r} не найден.'


class UserAlreadyExistsException(CreateError):
    """Ошибка создания нового пользователя из-за наличия такового."""

    def __init__(
        self,
        username: str = '',
    ):
        self._id = username
        super().__init__(self.detail)

    @property
    def detail(self):
        return f'Пользователь с username={self._id!r} уже существует.'


class InvalidPasswordToSet(CreateError):
    """Ошибка установки пароля пользователя."""

    @property
    def detail(self):
        return f'Ошибка установки пароля пользователя.'


class ForbiddenCreate(CreateError):
    """Ошибка создания нового объекта из-за отсутствия прав."""


class ForbiddenUpdate(UpdateError):
    """Ошибка обновления объекта из-за отсутствия прав."""


class UserPermissionsError(PermissionsError):
    """Ошибка доступа к данным и сервисам в связи с отсутствием прав пользователя."""



    # def __init__(
    #     self,
    #     requestor: str = '',
    # ):
    #     self.requestor = requestor
    #     super().__init__(self.detail)
    #
    # @property
    # def detail(self):
    #     return f'Отсутствуют права у {self.requestor!r}.'
