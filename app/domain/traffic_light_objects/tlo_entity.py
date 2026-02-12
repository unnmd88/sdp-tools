from datetime import datetime

from domain.kernel.business_rules import MIN_LEN_TLO_NAME, MAX_LEN_TLO_NAME
from domain.contract2.contract_field import ContractField
from domain.contract2.contract_field_enum import ContractFieldEnum
from domain.contract2.require import Require
from domain.kernel.base_entity import Entity
from domain.kernel.enums.controller_modes import ControllerModes
from domain.kernel.enums.snmp_protocols import SnmpProtocols
from domain.kernel.enums.unsorted import ServiceOrganizations
from domain.regions.region_entity import RegionEntity
from domain.kernel.entities_public_attrs import TRAFFIC_LIGHT_OBJECTS_PUBLIC_ATTRS
from domain.kernel.enums.controller_types import ControllerTypes
from domain.exceptions import DomainContractViolationError
from domain.validators.string_validator import StringValidator
from domain.value_objects.type_controller_vo import TypeControllerVO

"""
Поля:
    - id: int primary key
    - region: reference to region. RegionEntity
    - name : string номер светофора
    - type_controller: str VO тип контроллера
    - district: str VO округ
    - address: str VO адрес
    - service_organization: str VO обслуживающая организация
    - coordinates: VO tuple[float latitude, float longitude] координаты
    - status: str текущий статус
    - network: VO str сетевые настройки+оборудование
    - description: str описание
    - updated_at: datetime
    - created_at: datetime
    
    Перспективные поля:
    - peripheral: list[str] VO периферийных устройств(КИП-Д, Moxa, ...)
    
    
"""


class TrafficLightObjectEntity(Entity):
    """ Сущность светофорного объекта. """

    __public_attrs__ = TRAFFIC_LIGHT_OBJECTS_PUBLIC_ATTRS

    def __init__(
        self,
        *,
        id: int | None,
        region_id: int,
        created_by_user_id: int,
        updated_by_user_id: int | None,
        name: str,
        traffic_controller_type: str | None, # api дира
        latitude: float,
        longitude: float,
        district: str,
        address: str,
        note: str,
        created_at: datetime | None,
        updated_at: datetime | None,
    ):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        self.region_id = region_id
        self.traffic_controller_type = traffic_controller_type
        self.created_by_user_id = created_by_user_id
        self.updated_by_user_id = updated_by_user_id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.district = district
        self.address = address
        self.note = note
