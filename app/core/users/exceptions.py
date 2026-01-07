"""
Модуль, содержащий уточняющие исключения.
"""

from core.exceptions.base import (
    ApplicationError,
    NotFoundError,
    CreateError, UpdateError, )

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


class UserNotFoundError(NotFoundError):
    """Ошибка поиска user."""

    @property
    def detail(self):
        return f'Пользователь не найден.'


class UserAdministratorNotFoundError(NotFoundError):
    """Ошибка поиска пользователя-администратора."""


class UserNotFoundByIdError(UserNotFoundError):
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


class UserNotFoundByUsernameError(UserNotFoundError):
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


class UserAlreadyExistsError(CreateError):
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


class InvalidValueToSetError(CreateError):
    """Ошибка создания нового пользователя из-за невалидного username."""


class InvalidUsernameOrPasswordToSetError(ApplicationError):
    """Ошибка установки пароля пользователя."""

    @property
    def detail(self):
        return f'Ошибка установки username/пароля пользователя.'




class SameUsernameAndPasswordError(ApplicationError):
    """Ошибка совпадения username и пароля пользователя."""


class ForbiddenCreateError(CreateError):
    """Ошибка создания нового объекта из-за отсутствия прав."""


class ForbiddenUpdateError(UpdateError):
    """Ошибка обновления объекта из-за отсутствия прав."""


class InvalidUsernameOrPasswordError(ApplicationError):
    def __init__(self, user: str | int = ""):
        self.detail = f'Неверный логин или пароль пользователя {user}.'.replace("  ", "")
        super().__init__(self.detail)


class InactiveUserError(ApplicationError):
    ...
