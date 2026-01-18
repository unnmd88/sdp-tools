from dataclasses import dataclass

from domain.enums.unsorted import PeripheralEquipmentsTypes
from domain.tlo.value_objects.network_settings import NetworkSettings


@dataclass(frozen=True, slots=True)
class PeripheralEquipment:
    typ: PeripheralEquipmentsTypes
    network_settings: NetworkSettings
    description: str = ""
