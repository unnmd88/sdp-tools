from dataclasses import dataclass

from domain.enums.unsorted import ControllerTypes
from domain.tlo.value_objects.network_settings import NetworkSettings


@dataclass(frozen=True, slots=True)
class TrafficController:
    model: ControllerTypes
    network_settings: NetworkSettings
