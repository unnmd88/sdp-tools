from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import datetime
from typing import final

from core.enums import ServiceOrganizations, RegionNames
from core.passports.entities.passport import Passport


@final
@dataclass(frozen=True, slots=True, kw_only=True, order=True)
class TrafficLightObjectEntity:
    id: int
    region: RegionNames
    name: str
    district: str
    street: str
    service_organization: ServiceOrganizations
    description: str
    editing_now: bool
    current_passport: Passport
    passport_history: Sequence[Passport] = field(default_factory=list)
    created_at: datetime
    updated_at: datetime
