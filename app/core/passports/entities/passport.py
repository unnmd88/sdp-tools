from dataclasses import dataclass
from datetime import datetime
from typing import final

from core.enums import PassportGroups
from core.users.entities.user import UserEntity
from core.exceptions.base import DomainValidationError


@final
@dataclass(frozen=True, slots=True, kw_only=True, order=True)
class PassportEntity:
    data: dict
    username: str
    group_name: PassportGroups
    editing_now: bool
    commit_message: str
    started_editing_at: datetime
    finished_editing_at: datetime | None

    # def __post_init__(self):
    #     if not isinstance(self.username, UserEntity):
    #         raise DomainValidationError(
    #             f'Поле created_by должно экземпляр {UserEntity.__name__!r}'
    #         )

    # TO DO: validate rules
