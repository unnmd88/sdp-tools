from dataclasses import dataclass

from domain.enums.unsorted import PassportGroups


@dataclass(frozen=True, slots=True, kw_only=True)
class PassportGroupEntity:
    id: int | None = None
    group_name: PassportGroups
    description: str = ""

    # def __post_init__(self):
    #     if not check_description_is_valid(self.description):
    #         raise DomainValidationError(INVALID_DESCRIPTION_EXCEPTION_TEXT)
