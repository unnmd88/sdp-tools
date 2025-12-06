"""
Модуль, содержащий уточняющие исключения.
"""

from core.exceptions.base import (
    ApplicationException,
    NotFoundException,
    CreateException,
)

INVALID_DESCRIPTION_EXCEPTION_TEXT = (
    'Поле description не должно превышать 255 символов.'
)


class DomainValidationException(ApplicationException):
    """Ошибка валидации доменной сущности."""

    @property
    def detail(self):
        return f'Ошибка валидации. {". ".join(self.args)}'


class UserNotFoundException(NotFoundException):
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


class UserAlreadyExistsException(CreateException):
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


class InvalidPasswordToSet(CreateException):
    """Ошибка установки пароля пользователя."""

    @property
    def detail(self):
        return f'Ошибка установки пароля пользователя.'


class ForbiddenCreate(CreateException):
    """Ошибка создания нового объекта из-за отсутствия прав."""

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
