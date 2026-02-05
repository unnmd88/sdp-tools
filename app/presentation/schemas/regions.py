from datetime import datetime, timedelta
from typing import Annotated

from annotated_types import MinLen, MaxLen


from pydantic import BaseModel, ConfigDict, model_validator, Field


class RegionCreateSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    code: Annotated[int, Field(gt=0), Field(lt=65535)]
    name: Annotated[str, MinLen(3), MaxLen(32)]


class RegionSchemaResponse(RegionCreateSchema):
    model_config = ConfigDict(extra="ignore")

    id: int


class RegionUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # code_or_name: int | str

    name: Annotated[str | None, MinLen(3), MaxLen(32), Field(default=None)]
    code: Annotated[int | None, Field(gt=0), Field(lt=65535), Field(default=None)]

    @model_validator(mode="after")
    def check_has_data_for_update(self):
        if self.name is None and self.code is None:
            raise ValueError("Нет данных для обновления")
        return self
