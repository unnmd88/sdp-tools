from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import datetime
from typing import final

from core.enums import ServiceOrganizations, RegionNames

from core.passports.entities.passport import PassportEntity
from core.tlo.entities.traffic_controller import TrafficController
from core.tlo.value_objects.peripheral_equipments import PeripheralEquipment


@final
@dataclass(frozen=True, slots=True, kw_only=True, order=True)
class TrafficLightObjectEntity:
    id: int
    name: str
    region: RegionNames
    latitude: float
    longitude: float
    district: str
    street: str
    service_organization: ServiceOrganizations
    traffic_controller: TrafficController | None
    peripheral_equipments: Sequence[PeripheralEquipment] = field(default_factory=list)
    description: str
    editing_now: bool = False
    current_passport: PassportEntity | None
    passport_history: Sequence[PassportEntity] = field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    # def __post_init__(self):
    #     check_is_valid_enum(RegionNames, self.region)
    #     if not check_tlo_name_is_valid(self.name):
    #         raise DomainValidationError(
    #             'Недопустимый округ для светофорного объекта. '
    #             'Используйте буквы/цифры/тире/нижние подчёркивания без пробелов'
    #         )
    #     if not check_tlo_district_is_valid(self.district):
    #         raise DomainValidationError(
    #             'Недопустимый округ для светофорного объекта. Примеры допустимых округов: ЦАО, ВАО, ЮЗАО и т.д.'
    #         )
    #     # if not check_tlo_street_is_valid(self.street):
    #     #     raise DomainValidationError(
    #     #         'Недопустимое имя улицы. Используйте от 3 до 255 символов для названия.'
    #     #     )
    #     for coordinate in (self.latitude, self.longitude):
    #         if not check_tlo_latitude_or_longitude_is_valid(coordinate):
    #             raise DomainValidationError('Некорректные координаты широты/долготы.')
    #     if not isinstance(self.editing_now, bool):
    #         raise TypeError('attr editing_now must be a bool.')
    #     if not isinstance(self.current_passport, (PassportEntity | None)):
    #         raise TypeError(
    #             'attr current_passport must be a "Passport" instance or None.'
    #         )
    #     if self.passport_history:
    #         if any(
    #             not isinstance(instance, PassportEntity)
    #             for instance in self.passport_history
    #         ):
    #             raise TypeError(
    #                 'all elements of attr passport_history must be a "Passport" instance.'
    #             )
