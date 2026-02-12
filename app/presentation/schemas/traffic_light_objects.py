from pydantic import BaseModel, ConfigDict, Field


class TrafficLightObjectCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    region_id: int
    name: str
    traffic_controller_type: str | None
    latitude: float
    longitude: float
    district: str
    address: str
    note: str