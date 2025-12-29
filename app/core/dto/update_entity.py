from dataclasses import dataclass, field
from typing import Any


@dataclass
class UpdatedEntityDTO:

    old: Any
    new: Any

    name: str | None = None


    # TODO
    # count_updated_fields: int
    # updated_fields: list = field(default_factory=list)
