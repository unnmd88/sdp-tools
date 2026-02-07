from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict

from domain.enums.unsorted import PassportGroups


class PassportGroupsBase(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    name: PassportGroups
    description: Annotated[str, Field(default="")]


class PassportGroupResponse(PassportGroupsBase):
    id: Annotated[int, Field(ge=1)]


class PassportGroupsCreate(PassportGroupsBase):
    """Create passport group"""


class PassportGroupsUpdate(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )

    group_name_to_update: PassportGroups

    group_name: PassportGroups | None = None
    description: Annotated[str | None, Field(default=None)]
