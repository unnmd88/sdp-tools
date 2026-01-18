from dataclasses import dataclass

from domain.enums.unsorted import PassportGroups


@dataclass(kw_only=True)
class PassportGroupDTO:
    group_name: PassportGroups
    description: str


@dataclass(kw_only=True)
class UpdatePassportGroupDTO:
    group_name_to_update: PassportGroups

    group_name: PassportGroups | None = None
    description: str | None = None


@dataclass(kw_only=True)
class CreatePassportGroupDTO:
    group_name: PassportGroups
    description: str | None = ""
