from typing import Annotated

from annotated_types import MinLen, MaxLen

from core.constants import ALLOWED_REGIONS
from pydantic import BaseModel, ConfigDict, model_validator, Field


class RegionCreate(BaseModel):

    name: Annotated[str, MinLen(3), MaxLen(32)]
    code: Annotated[int, Field(gt=0), Field(lt=65535)]

    # @model_validator(mode='after')
    # def check_allowed_pair_name_region(self):
    #     if (self.name, self.code) not in ALLOWED_REGIONS:
    #         raise ValueError('Некорректная пара имя-регион')
    #     return self


class RegionSchema(RegionCreate):
    id: Annotated[int, Field(gt=0)]


class RegionUpdate(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    code_or_name: int | str

    name: Annotated[str | None, MinLen(3), MaxLen(32), Field(default=None)]
    code: Annotated[int | None, Field(gt=0), Field(lt=65535), Field(default=None)]

    @model_validator(mode='after')
    def check_pair(self):
        if self.name is None and self.code is None:
            raise ValueError('Нет данных для обновления')
        return self