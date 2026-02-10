from dataclasses import dataclass


@dataclass(slots=True, kw_only=True, frozen=True)
class RegionVo:
    code: int
    name: str