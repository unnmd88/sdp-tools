from pydantic import BaseModel, ConfigDict, AfterValidator
from sqlalchemy.sql.annotation import Annotated

from core.constants import RegionCodes, RegionNames


class CreateRegionSchema(BaseModel):
    name: RegionNames
    code: RegionCodes


class RegionSchema(CreateRegionSchema):
    id: int


class RegionUpdateSchema(CreateRegionSchema):
    name: RegionNames = None
    code: RegionCodes = None