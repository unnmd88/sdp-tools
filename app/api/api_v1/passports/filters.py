from typing import Annotated

from pydantic import BaseModel, Field

from core.constants import PassportGroupsRoutes, PassportGroups


class PassportGroupIdFilter(BaseModel):
    group_id: Annotated[int, Field(ge=1)]


class PassportGroupNameRouteAndTloNameFilter(BaseModel):
    group_name: str
    tlo_name: str


class PassportCurrentFilter(BaseModel):
    group_id: Annotated[int, Field(ge=1)]
    tlo_id: Annotated[int, Field(ge=1)]