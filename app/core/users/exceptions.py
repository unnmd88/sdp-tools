from dataclasses import dataclass
from typing import final

from core.exceptions.base import ApplicationException, NotFoundException


@dataclass
class DomainValidationException(ApplicationException):
    """
    Ошибка валидации доменной сущности.
    """

    detail: str = 'Ошибка валидации объекта домена.'


@final
@dataclass
class UserNotFoundException(NotFoundException):
    user: str | int = ''

    @property
    def detail(self) -> str:
        return f'Пользователь {self.user!r} не найден'.replace('  ', ' ')
