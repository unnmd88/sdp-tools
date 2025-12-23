from dataclasses import dataclass

from core.enums import (
    PassportGroups,
    PassportGroupsRoutes
)


@dataclass(kw_only=True)
class PassportGroupsDTO:
    group_name: PassportGroups
    group_name_route: PassportGroupsRoutes
    description: str


@dataclass(kw_only=True)
class UpdatePassportGroupsDTO:

    group_name_to_update: PassportGroups

    group_name: PassportGroups | None = None
    group_name_route: PassportGroupsRoutes | None = None
    description: str | None = None


@dataclass(kw_only=True)
class CreatePassportGroupsDTO:

    group_name: PassportGroups
    group_name_route: PassportGroupsRoutes
    description: str | None = ''