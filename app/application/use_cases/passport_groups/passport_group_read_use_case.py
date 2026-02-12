from dataclasses import dataclass

from application.dto.passport_groups_dto import PassportGroupDTO
from application.interfaces.services.passport_groups_service_interface import (
    PassportGroupReadServiceProtocol,
)


@dataclass(slots=True, kw_only=True, frozen=True)
class PassportGroupReadByNameUseCase:
    pg_service: PassportGroupReadServiceProtocol

    async def __call__(self, passport_group_name: str) -> PassportGroupDTO:
        entity = await self.pg_service.get_by_name(passport_group_name)
        return PassportGroupDTO.from_entity(entity)
