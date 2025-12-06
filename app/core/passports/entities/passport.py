from dataclasses import dataclass
from typing import final

from core.enums import PassportGroups
from core.users.entities.user import UserEntity
from core.users.exceptions import DomainValidationException


@final
@dataclass(frozen=True, slots=True, kw_only=True, order=True)
class Passport:
    data: dict
    created_by: UserEntity
    group: PassportGroups
    commit_message: str

    def __post_init__(self):
        if not isinstance(self.created_by, UserEntity):
            raise DomainValidationException(
                f'Поле created_by должно экземпляр {UserEntity.__name__!r}'
            )

    # TO DO: validate rules
