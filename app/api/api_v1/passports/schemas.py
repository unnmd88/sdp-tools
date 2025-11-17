from datetime import datetime
from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, Field, computed_field


class PassportGroupBase(BaseModel):
    tlo_name: Annotated[str, MinLen(2)]
    user_id: Annotated[int, Field(ge=1)]
    group_id: Annotated[int, Field(ge=1)]


class CapturePassport(PassportGroupBase):
    pass


class CapturedPassport(PassportGroupBase):
    id: Annotated[int, Field(ge=1)]


class SavePassport(PassportGroupBase):
    id: Annotated[int, Field(ge=1, exclude=True)]
    # tlo_id: Annotated[int, Field(ge=1, exclude=True)]
    # user_id: Annotated[int, Field(ge=1, exclude=True)]
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


class SavedPassportSchema(BaseModel):
    tlo_id: Annotated[int, Field(ge=1)]
    group_id: Annotated[int, Field(ge=1)]
    # user_id: Annotated[int, Field(ge=1)]
    finished_editing_at: datetime
    editing_now: bool


class CurrentPassportSchema(BaseModel):
    id: Annotated[int, Field(ge=1)]
    tlo_id: Annotated[int, Field(ge=1)]
    user_id: Annotated[int, Field(ge=1)]
    group_id: Annotated[int, Field(ge=1)]
    data: dict
    commit_message: str
    editing_now: bool
    started_editing_at: datetime
    finished_editing_at: datetime
