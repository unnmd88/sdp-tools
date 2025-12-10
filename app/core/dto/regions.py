from dataclasses import dataclass

from core.enums import RegionCodes, RegionNames


@dataclass(kw_only=True)
class RegionsDTO:
    code: RegionCodes
    name: RegionNames


@dataclass(kw_only=True)
class UpdateRegionsDTO:

    region_name_to_update: RegionNames

    code: RegionCodes | None = None
    name: RegionNames | None = None


@dataclass(kw_only=True)
class CreateRegionsDTO:

    code: RegionCodes
    name: RegionNames