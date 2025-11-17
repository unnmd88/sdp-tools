from typing import Annotated

from pydantic import BaseModel, Field

from core.constants import PassportGroupsRoutes, PassportGroups


class PassportGroupIdFilter(BaseModel):
    group_id: Annotated[int, Field(ge=1)]


class PassportGroupNameRouteFilter(BaseModel):
    group_name_route: Annotated[str, PassportGroupsRoutes]


class PassportGroupNameFilter(BaseModel):
    group_name: Annotated[str, PassportGroups]


class PassportCurrentFilter(BaseModel):
    group_id: Annotated[int, Field(ge=1)]
    tlo_id: Annotated[int, Field(ge=1)]