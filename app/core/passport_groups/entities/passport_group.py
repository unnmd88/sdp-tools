from dataclasses import dataclass

from core.enums import RegionCodes, RegionNames, PassportGroups, PassportGroupsRoutes
from core.field_validators import check_is_valid_enum, check_description_is_valid
from core.users.exceptions import (
    DomainValidationException,
    INVALID_DESCRIPTION_EXCEPTION_TEXT,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class PassportGroup:
    id: int
    group_name: PassportGroups
    group_name_route: PassportGroupsRoutes
    description: str = ''

    def __post_init__(self):
        check_is_valid_enum(RegionCodes, self.group_name)
        check_is_valid_enum(RegionCodes, self.group_name_route)
        if not check_description_is_valid(self.description):
            raise DomainValidationException(INVALID_DESCRIPTION_EXCEPTION_TEXT)
