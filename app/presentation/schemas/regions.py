from core.constants import ALLOWED_REGIONS
from core.enums import RegionCodes, RegionNames
from pydantic import BaseModel, ConfigDict, model_validator


class RegionCreate(BaseModel):
    name: RegionNames
    code: RegionCodes

    @model_validator(mode='after')
    def check_allowed_pair_name_region(self):
        if (self.name, self.code) not in ALLOWED_REGIONS:
            raise ValueError('Некорректная пара имя-регион')
        return self


class RegionSchema(RegionCreate):
    id: int


class RegionUpdate(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    region_name_to_update: RegionNames
    name: RegionNames | None = None
    code: RegionCodes | None = None

    @model_validator(mode='after')
    def check_pair(self):
        if self.name is None and self.code is None:
            raise ValueError('Нет данных для обновления')
        return self