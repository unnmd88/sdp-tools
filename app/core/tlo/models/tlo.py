from datetime import datetime
from dataclasses import dataclass

from core.enums import ServiceOrganizations


@dataclass
class TrafficLightObject:
    id: int
    region_id: int
    name: str
    district: str
    street: str
    service_organization: ServiceOrganizations
    description: str
    created_at: datetime
    updated_at: datetime
