from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import datetime
from typing import final

from core.enums import ServiceOrganizations, RegionNames, EntityIdRange
from core.field_validators import check_is_valid_enum, check_field_id_is_valid, check_tlo_name_is_valid, \
    check_tlo_district_is_valid, check_tlo_street_is_valid, check_tlo_latitude_or_longitude_is_valid
from core.passports.entities.passport import Passport
from core.users.exceptions import DomainValidationError


@final
@dataclass(frozen=True, slots=True, kw_only=True, order=True)
class TrafficLightObjectEntity:
    id: int
    region: RegionNames
    name: str
    district: str
    street: str
    latitude: float
    longitude: float
    service_organization: ServiceOrganizations
    description: str
    current_passport: Passport | None
    passport_history: Sequence[Passport] = field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        check_is_valid_enum(RegionNames, self.region)
        if not check_tlo_name_is_valid(self.name):
            raise DomainValidationError(
                'Недопустимый округ для светофорного объекта. '
                'Используйте буквы/цифры/тире/нижние подчёркивания без пробелов'
            )
        if not check_tlo_district_is_valid(self.district):
            raise DomainValidationError(
                'Недопустимый округ для светофорного объекта. Примеры допустимых округов: ЦАО, ВАО, ЮЗАО и т.д.'
            )
        if not check_tlo_street_is_valid(self.street):
            raise DomainValidationError(
                'Недопустимое имя улицы. Используйте от 3 до 255 символов для названия.'
            )
        for coordinate in (self.latitude, self.longitude):
            if not check_tlo_latitude_or_longitude_is_valid(coordinate):
                raise DomainValidationError('Некорректные координаты широты/долготы.')

