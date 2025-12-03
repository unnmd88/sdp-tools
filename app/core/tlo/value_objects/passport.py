from dataclasses import dataclass
from typing import final

from core.enums import PassportGroups


@final
@dataclass(frozen=True, slots=True, kw_only=True, order=True)
class Passport:

    data: dict
    created_by: str
    group: PassportGroups
    commit_message: str

    # TO DO: validate rules