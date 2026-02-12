from dataclasses import dataclass
from datetime import datetime

from domain.kernel.enums.unsorted import ServiceOrganizations


@dataclass
class TrafficLightObjectDTO:
    id: int
    region_id: int
    name: str
    type_controller: str
    snmp_protocol: str
    district: str
    address: str
    lat: float
    lon: float
    network: dict
    status: str
    service_organization: ServiceOrganizations
    note: str
    created_at: datetime
    updated_at: datetime

