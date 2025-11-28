from dataclasses import dataclass
from typing import final

from core.exceptions.base import NotFoundException


@final
@dataclass
class UserNotFoundException(NotFoundException):

    user: str | int = ''

    @property
    def detail(self) -> str:
        return f"User {self.user!r} not found".replace("  ", " ")

