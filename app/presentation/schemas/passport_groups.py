from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict


class PassportGroupsBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    description: str


class PassportGroupResponse(PassportGroupsBase):
    id: Annotated[int, Field(ge=1)]


class PassportGroupsCreate(PassportGroupsBase):
    """Create passport group"""


class PassportGroupsUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    new_name: str | None = Field(default=None, min_length=3, max_length=32)
    new_description: Annotated[str | None, Field(default=None)]
