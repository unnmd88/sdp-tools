from dataclasses import dataclass
from application.dto.passport_groups import PassportGroupDTO
from application.interfaces.services.passport_groups_service_interface import PassportGroupServiceProtocol
from domain.exceptions import DomainEntityNotFoundError


@dataclass(frozen=True, slots=True, kw_only=True)
class ReadPassportGroupUseCaseImpl:
    passport_groups_service: PassportGroupServiceProtocol

    async def by_id(self, passport_group_id: int) -> PassportGroupDTO:
        passport_group = await self.passport_groups_service.get_passport_group_by_id(passport_group_id)
        if passport_group is None:
            raise DomainEntityNotFoundError(public_message="Группа паспортов не найдена.")
        else:
            return PassportGroupDTO.from_entity(passport_group)

    async def by_name(self, name: str) -> PassportGroupDTO:
        region = await self.passport_groups_service.get_passport_group_by_name(
            name=name,
            raise_if_not_found=True,
        )
        return PassportGroupDTO.from_entity(region)