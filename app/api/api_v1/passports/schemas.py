from datetime import datetime
from typing import Annotated

from annotated_types import MaxLen
from pydantic import BaseModel, Field, computed_field


class CapturePassport(BaseModel):
    tlo_id: Annotated[int, Field(ge=1)]
    user_id: Annotated[int, Field(ge=1)]


class SavePassport(BaseModel):
    id: Annotated[int, Field(ge=1, exclude=True)]
    tlo_id: Annotated[int, Field(ge=1, exclude=True)]
    user_id: Annotated[int, Field(ge=1, exclude=True)]
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
    # user_id: Annotated[int, Field(ge=1)]
    finished_editing_at: datetime
    editing_now: bool


class PassportSchema(BaseModel):
    tlo_id: Annotated[int, Field(ge=1)]