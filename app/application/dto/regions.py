from dataclasses import dataclass, field
from datetime import datetime
from typing import TypedDict


@dataclass(slots=True, frozen=True, kw_only=True)
class RegionDTO:
    """DTO для экземпляра существующего региона."""

    id: int
    code: int
    name: str
    built_at: str | datetime
    created_at: str | None
    updated_at: str | None

    @classmethod
    def from_entity(cls, entity):
        return cls(**entity.to_dict())


class UpdateRegionDTO(TypedDict):
    """ DTO для обновления существующего региона. """
    name: str
    code: int


@dataclass(slots=True, frozen=True, kw_only=True)
class UpdateRegionDTO:
    """DTO для обновления существующего региона."""

    # region_name_to_update: RegionNames
    filters_for_search: dict
    code_or_name: str

    code: int | None = None
    name: str | None = None


@dataclass(slots=True, frozen=True, kw_only=True)
class CreateRegionDTO(RegionDTO):
    """DTO для создания нового региона."""
