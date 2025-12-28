from dataclasses import dataclass

from core.enums import PeripheralEquipmentsTypes
from core.tlo.value_objects.network_settings import NetworkSettings


@dataclass(frozen=True, slots=True)
class PeripheralEquipment:

    typ: PeripheralEquipmentsTypes
    network_settings: NetworkSettings
    description: str = ''