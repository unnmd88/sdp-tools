from typing import Annotated

from annotated_types import MaxLen
from pydantic import BaseModel, Field


class CreatePassport(BaseModel):
    tlo_id: Annotated[int, Field(ge=1)]
    user_id: Annotated[int, Field(ge=1)]
    data: dict
    commit_message: Annotated[str, MaxLen(255)]


class PassportSchema(BaseModel):
    tlo_id: Annotated[int, Field(ge=1)]