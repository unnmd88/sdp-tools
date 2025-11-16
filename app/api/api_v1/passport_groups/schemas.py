from typing import Annotated
from pydantic import BaseModel, Field

from core.constants import PassportGroups, PassportGroupsRoutes


class PassportBase(BaseModel):
    group_name: PassportGroups
    group_name_route: PassportGroupsRoutes
    description: Annotated[str, Field(default='')]


class PassportGroupsSchema(PassportBase):
    id: Annotated[int, Field(ge=1)]


class PassportGroupsCreate(PassportBase):
    pass


class PassportGroupsUpdate(PassportBase):
    pass
