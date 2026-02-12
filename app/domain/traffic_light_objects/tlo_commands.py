from dataclasses import dataclass
from typing import ClassVar


@dataclass(slots=True, kw_only=True, frozen=True)
class CreateTrafficLightObjectCommand:
    operation_name: ClassVar[str] = "Создать новый светофорный объект"
    customer_id: int

    region_id: int
    name: str
    created_by_user_id: int
    updated_by_user_id: int
    traffic_controller_type: str | None  # api дира
    latitude: float
    longitude: float
    district: str
    address: str
    note: str


@dataclass(slots=True, kw_only=True, frozen=True)
class UpdateTrafficLightObjectCommand:
    operation_name: ClassVar[str] = "Обновить существующий светофорный объект"
    customer_id: int
    tlo_name: str

    region_id: int
    created_by_user_id: int
    updated_by_user_id: int
    name: str
    traffic_controller_type: str | None  # api дира
    latitude: float
    longitude: float
    district: str
    address: str
    note: str


@dataclass(slots=True, kw_only=True, frozen=True)
class DeleteTrafficLightObjectCommand:
    """Удаление светофорного объекта"""
    operation_name: ClassVar[str] = "Удалить регион"
    customer_id: int

    tlo_name: str

