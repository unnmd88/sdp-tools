from datetime import datetime
from typing import Annotated

from annotated_types import MaxLen, MinLen
from core.enums import (
    PassportGroups,
    RegionCodes,
    RegionNames,
    ServiceOrganizations,
)
from pydantic import BaseModel, Field, computed_field


class PassportSchemaBase(BaseModel):
    # user_id: Annotated[int, Field(ge=1)]
    tlo_name: Annotated[str, MinLen(2)]
    group_name: PassportGroups


class CapturePassportSchema(PassportSchemaBase):
    pass


class CapturePassportSchemaSaveToDatabase(BaseModel):
    user_id: Annotated[int, Field(ge=1)]
    tlo_id: Annotated[int, Field(ge=1)]
    group_id: Annotated[int, Field(ge=1)]


class CapturedPassport(PassportSchemaBase):
    id: Annotated[int, Field(ge=1)]
    username: str
    editing_now: bool


class UpdatePassport(PassportSchemaBase):
    id: Annotated[int, Field(ge=1, exclude=True)]
    data: dict
    commit_message: Annotated[str, MaxLen(255)]


class UpdatePassportSchemaSaveToDatabase(BaseModel):
    id: Annotated[int, Field(ge=1, exclude=True)]
    user_id: Annotated[int, Field(ge=1)]
    tlo_id: Annotated[int, Field(ge=1)]
    group_id: Annotated[int, Field(ge=1)]
    data: dict
    commit_message: Annotated[str, MaxLen(255)]

    @computed_field
    @property
    def finished_editing_at(self) -> datetime:
        return datetime.now()

    @computed_field
    @property
    def editing_now(self) -> bool:
        return False


class FinalSavedPassportSchema(BaseModel):
    id: Annotated[int, Field(ge=1)]
    tlo_name: Annotated[str, MinLen(1)]
    group_name: PassportGroups
    username: str
    editing_now: bool


class CurrentPassportSchema(BaseModel):
    # id: Annotated[int, Field(ge=1)]
    tlo_name: str
    region_code: RegionCodes
    region_name: RegionNames
    street: str
    service_organization: ServiceOrganizations
    username: str
    passport_group_name: str
    data: dict
    commit_message: str
    editing_now: bool | dict
    started_editing_at: datetime
    finished_editing_at: datetime


# class CurrentPassportSchema(BaseModel):
#     id: Annotated[int, Field(ge=1)]
#     tlo_id: Annotated[int, Field(ge=1)]
#     user_id: Annotated[int, Field(ge=1)]
#     group_id: Annotated[int, Field(ge=1)]
#     data: dict
#     commit_message: str
#     editing_now: bool
#     started_editing_at: datetime
#     finished_editing_at: datetime
