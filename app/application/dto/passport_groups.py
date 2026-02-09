from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True, kw_only=True)
class PassportGroupDTO:
    id: int
    name: str
    description: str
    built_at: str | datetime
    created_at: str | None | datetime
    updated_at: str | None | datetime

    @classmethod
    def from_entity(cls, entity):
        return cls(**entity.to_dict())
