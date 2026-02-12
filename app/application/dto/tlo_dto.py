from dataclasses import dataclass
from datetime import datetime

from domain.kernel.enums.unsorted import ServiceOrganizations


@dataclass
class TrafficLightObjectDTO:
    id: int
    region_id: int
    created_by_user_id: int
    updated_by_user_id: int
    name: str
    traffic_controller_type: str
    latitude: float
    longitude: float
    district: str
    address: str
    note: str
    built_at: datetime
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, entity):
        return cls(**entity.to_dict())

