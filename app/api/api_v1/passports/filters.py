from typing import Annotated

from pydantic import BaseModel, Field

from core.constants import PassportGroupsRoutes


class PassportGroupIdFilter(BaseModel):
    group_id: Annotated[int, Field(ge=1)]


class PassportGroupNameFilter(BaseModel):
    group_name_route: Annotated[str, PassportGroupsRoutes]


class PassportCurrentFilter(BaseModel):
    group_id: Annotated[int, Field(ge=1)]
    tlo_id: Annotated[int, Field(ge=1)]