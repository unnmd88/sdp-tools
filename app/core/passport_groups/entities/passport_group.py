from dataclasses import dataclass

from core.enums import PassportGroups
from core.field_validators import check_is_valid_enum, check_description_is_valid
from core.users.exceptions import (
    DomainValidationError,
    INVALID_DESCRIPTION_EXCEPTION_TEXT,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class PassportGroupEntity:

    id: int | None = None
    group_name: PassportGroups
    description: str = ''

    def __post_init__(self):
        check_is_valid_enum(PassportGroups, self.group_name)
        if not check_description_is_valid(self.description):
            raise DomainValidationError(INVALID_DESCRIPTION_EXCEPTION_TEXT)
