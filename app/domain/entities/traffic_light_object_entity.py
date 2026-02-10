from datetime import datetime

from domain.business_rules import MIN_LEN_TLO_NAME, MAX_LEN_TLO_NAME
from domain.contract2.contract_field import ContractField
from domain.contract2.contract_field_enum import ContractFieldEnum
from domain.contract2.require import Require
from domain.entities.base_entity import Entity
from domain.entities.region_entity import RegionEntity
from domain.entities_public_attrs import TRAFFIC_LIGHT_OBJECTS_PUBLIC_ATTRS
from domain.enums.attrs_names import PublicAttrNamesEnum
from domain.enums.controller_modes import ControllerModes
from domain.enums.controller_types import ControllerTypes
from domain.enums.snmp_protocols import SnmpProtocols
from domain.enums.unsorted import ServiceOrganizations
from domain.exceptions import DomainContractViolationError
from domain.validators.positive_int_validator import IntegerValidator
from domain.validators.string_validator import StringValidator
from domain.value_objects.address_vo import AddressVO
from domain.value_objects.region_vo import RegionVo
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
    - main_mode: str VO основной режим работы
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
    __public_attrs__ = TRAFFIC_LIGHT_OBJECTS_PUBLIC_ATTRS

    name = ContractField(
        field_name=str(PublicAttrNamesEnum.name),
        nullable=False,
        use_cache=True,
        requires=[Require(handler=StringValidator(min_length=MIN_LEN_TLO_NAME, max_length=MAX_LEN_TLO_NAME))],
    )
    type_controller = ContractFieldEnum(
        field_name=str(PublicAttrNamesEnum.type_controller),
        nullable=True,
        enum=TypeControllerVO
    )

    def __init__(
        self,
        *,
        id: int | None,
        name: str,
        type_controller: str | ControllerTypes,
        general_mode: str | ControllerModes,
        snmp_protocol: str | SnmpProtocols,
        region: RegionEntity,
        district: str,
        address: str,
        service_organization: str | ServiceOrganizations,
        created_at: datetime | None,
        updated_at: datetime | None,

    ):
        super().__init__(id=id, created_at=None, updated_at=None)
        if not isinstance(region, RegionEntity):
            raise DomainContractViolationError(
                private_message=f"region должен быть экземпляром RegionEntity, а не {RegionEntity.__name__!r}",
                public_message=f"Ошибка валидации. Обратитесь к администратору.",
            )
        self.name = name
        self.region = region
        self.type_controller: ControllerTypes = type_controller
        self.general_mode: ControllerModes = general_mode
        self.snmp_protocol: SnmpProtocols = snmp_protocol
        self.district = district
        self.address = address
        self.service_organization: ServiceOrganizations = service_organization


    """ Сущность светофорного объекта. """