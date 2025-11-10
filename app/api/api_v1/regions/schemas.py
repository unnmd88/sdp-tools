from pydantic import BaseModel, ConfigDict, AfterValidator
from sqlalchemy.sql.annotation import Annotated

from core.constants import RegionCodes, RegionNames


class RegionCreate(BaseModel):
    name: RegionNames
    code: RegionCodes


class RegionSchema(RegionCreate):
    id: int


class RegionUpdate(RegionCreate):
    name: RegionNames | None = None
    code: RegionCodes | None = None