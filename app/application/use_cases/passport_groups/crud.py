from collections.abc import Sequence

from application.interfaces.services.passport_groups_crud import PassportGroupsServiceProtocol
from application.interfaces.services.regions_crud import RegionsServiceProtocol
from core.dto.passport_groups import CreatePassportGroupsDTO, UpdatePassportGroupsDTO
from core.dto.regions import CreateRegionsDTO, UpdateRegionsDTO
from core.passport_groups.entities.passport_group import PassportGroupEntity
from core.regions.entities.region import RegionEntity


class PassportGroupsCrudUseCaseImpl:
    def __init__(self, passport_group_service: PassportGroupsServiceProtocol):
        self.passport_group_service = passport_group_service

    async def get_passport_group_by_id(self, passport_group_id: int) -> PassportGroupEntity | None:
        return await self.passport_group_service.get_passport_group_by_id_or_none(passport_group_id)

    async def get_passport_group_by_name(self, name: str) -> PassportGroupEntity | None:
        return await self.passport_group_service.get_passport_group_by_name_or_none(name)

    async def get_all_passport_groups(self) -> Sequence[PassportGroupEntity]:
        return await self.passport_group_service.get_all_passport_groups()

    async def create_passport_group(self, passport_group: CreatePassportGroupsDTO) -> PassportGroupEntity:
       return await self.passport_group_service.create_passport_group(passport_group)

    async def update_passport_group(self, passport_group: UpdatePassportGroupsDTO) -> PassportGroupEntity:
        return await self.passport_group_service.update_passport_group(passport_group)

