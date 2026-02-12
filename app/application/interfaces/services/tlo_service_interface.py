from typing import Protocol

from application.interfaces.services.base_service_interface import BaseReadServiceProtocol, BaseWriteServiceProtocol
from domain.traffic_light_objects.tlo_commands import CreateTrafficLightObjectCommand, UpdateTrafficLightObjectCommand, \
    DeleteTrafficLightObjectCommand
from domain.traffic_light_objects.tlo_entity import TrafficLightObjectEntity


class TrafficLightObjectReadServiceProtocol(BaseReadServiceProtocol[TrafficLightObjectEntity], Protocol):
    async def get_by_name(self, name: str) -> TrafficLightObjectEntity: ...


# class TrafficLightObjectWriteServiceProtocol(
#     BaseWriteServiceProtocol[TrafficLightObjectEntity, CreateTrafficLightObjectCommand, UpdateTrafficLightObjectCommand, DeleteTrafficLightObjectCommand],
#     Protocol
# ):
#     # async def update(self, command) -> TrafficLightObjectEntity: ...
#     async def create(self, command: CreateTrafficLightObjectCommand) -> TrafficLightObjectEntity: ...
#     # async def delete(self, command) -> TrafficLightObjectEntity: ...


class TrafficLightObjectServiceProtocol(
    TrafficLightObjectReadServiceProtocol, BaseWriteServiceProtocol, Protocol
): ...
