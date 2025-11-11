from typing import Annotated

from annotated_types import MaxLen
from pydantic import BaseModel, Field, ConfigDict

from core.constants import ServiceOrganizations, Districts


class TrafficLightCreate(BaseModel):
    region_id: Annotated[int, Field(ge=1)]
    name: Annotated[str, MaxLen(32)]
    district: Districts
    street: str
    service_organization: ServiceOrganizations
    description: Annotated[str, Field(default='')]


class TrafficLightSchema(BaseModel):
    id: int
    region_id: Annotated[int, Field(ge=1)]
    name: str
    district: Districts
    street: str
    service_organization: ServiceOrganizations
    description: str


class TrafficLightUpdate(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )

    region_id: Annotated[int, Field(ge=1)] | None
    name: str | None
    district: Districts | None
    street: str | None
    service_organization: ServiceOrganizations | None
    description: str | None