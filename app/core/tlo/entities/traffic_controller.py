from dataclasses import dataclass

from core.enums import ControllerTypes
from core.tlo.value_objects.network_settings import NetworkSettings


@dataclass(frozen=True, slots=True)
class TrafficController:
    model: ControllerTypes
    network_settings: NetworkSettings
