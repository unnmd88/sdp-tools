from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from typing import final

from application.interfaces.mappers.db import BaseDBMapperProtocol
from core.dto.tlo import TrafficLightObjectDTO
from core.enums import ServiceOrganizations, RegionNames, ControllerTypes
from core.passports.entities.passport import PassportEntity
from core.tlo.entities.tlo import TrafficLightObjectEntity
from core.tlo.entities.traffic_controller import TrafficController
from core.tlo.value_objects.network_settings import NetworkSettings
from infrastructure.database.models import TrafficLightObject as TrafficLightObjectModel, TrafficLightObject


@final
@dataclass(frozen=True, slots=True)
class TrafficLightObjectDBMapper(BaseDBMapperProtocol):
    @classmethod
    def to_entity(cls, model: TrafficLightObjectModel) -> TrafficLightObjectEntity:
        """ """

        traffic_controller = TrafficController(
            model=ControllerTypes(model.traffic_controller),
            network_settings=NetworkSettings(
                ipv4=model.ipv4.ip if model.ipv4 is not None else None,
                network=model.ipv4.network if model.ipv4 is not None else None,
                mask=model.ipv4.netmask if model.ipv4 is not None else None,
                gateway=model.gateway.ip if model.gateway is not None else None,
                broadcast=model.ipv4.network.broadcast_address if model.gateway is not None else None,
                mac_address=model.mac_address,
            )
        )
        return TrafficLightObjectEntity(
            id=model.id,
            name=model.name,
            region=RegionNames.MOSCOW,
            latitude=model.latitude,
            longitude=model.longitude,
            district=model.district,
            street=model.street,
            service_organization=ServiceOrganizations(model.service_organization),
            traffic_controller=traffic_controller,
            current_passport=None,
            description=model.description,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @classmethod
    def to_full_entity(cls, tlo_model, passports: Sequence[PassportEntity]) -> TrafficLightObjectEntity:
        traffic_controller = TrafficController(
            model=ControllerTypes(tlo_model.traffic_controller),
            network_settings=NetworkSettings(
                ipv4=tlo_model.ipv4.ip if tlo_model.ipv4 is not None else None,
                network=tlo_model.ipv4.network if tlo_model.ipv4 is not None else None,
                mask=tlo_model.ipv4.netmask if tlo_model.ipv4 is not None else None,
                gateway=tlo_model.gateway.ip if tlo_model.gateway is not None else None,
                broadcast=tlo_model.ipv4.network.broadcast_address if tlo_model.gateway is not None else None,
                mac_address=tlo_model.mac_address,
            )
        )
        return TrafficLightObjectEntity(
            id=tlo_model.id,
            name=tlo_model.name,
            region=RegionNames.MOSCOW,
            latitude=tlo_model.latitude,
            longitude=tlo_model.longitude,
            district=tlo_model.district,
            street=tlo_model.street,
            service_organization=ServiceOrganizations(tlo_model.service_organization),
            traffic_controller=traffic_controller,
            current_passport=None,
            description=tlo_model.description,
            created_at=tlo_model.created_at,
            updated_at=tlo_model.updated_at,
        )

    # @classmethod
    # def to_model(cls, entity: RegionEntity) -> RegionModel:
    #     """ """
    #     if entity.id is None:
    #         return RegionModel(
    #             code=entity.code,
    #             name=entity.name,
    #         )
    #     return RegionModel(
    #         id=entity.id,
    #         code=entity.code,
    #         name=entity.name,
    #         )
