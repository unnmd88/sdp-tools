from pydantic import BaseModel, ConfigDict


from core.constants import RegionCodes, RegionNames


class RegionCreate(BaseModel):
    name: RegionNames
    code: RegionCodes


class RegionSchema(RegionCreate):
    id: int


class RegionUpdate(RegionCreate):
    model_config = ConfigDict(
        extra='forbid',
    )
    name: RegionNames | None = None
    code: RegionCodes | None = None