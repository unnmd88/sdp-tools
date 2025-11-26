from dataclasses import dataclass
from datetime import datetime

from core.constants import ServiceOrganizations


@dataclass
class TrafficLightObjectDTO:
    id: int
    region_id: int
    name: str
    district: str
    street: str
    service_organization: ServiceOrganizations
    description: str
    created_at: datetime
    updated_at: datetime