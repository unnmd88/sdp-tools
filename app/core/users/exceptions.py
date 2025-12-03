"""
Модуль, содержащий уточняющие исключения.
"""

from core.exceptions.base import (
    ApplicationException,
    NotFoundException,
)

INVALID_DESCRIPTION_EXCEPTION_TEXT= 'Поле description не должно превышать 255 символов.'


class DomainValidationException(ApplicationException):
    """ Ошибка валидации доменной сущности. """

    @property
    def detail(self):
        return f'Ошибка валидации. {". ".join(self.args)}'


class UserNotFoundException(NotFoundException):
    """ Ошибка поиска user. """

    @property
    def detail(self):
        return f'Пользователь не найден.'


class UserNotFoundByIdException(UserNotFoundException):
    """ Ошибка поиска user по id. """

    def __init__(
        self,
        user_id: int,
    ):
        self._id = user_id
        super().__init__(self.detail)

    @property
    def detail(self):
        return f'Пользователь с id={self._id!r} не найден.'


if __name__ == '__main__':
    raise UserNotFoundByIdException(1)