from collections.abc import Sequence
from dataclasses import asdict

from application.interfaces.repositories.passport_groups import PassportGroupRepositoryProtocol
from core.dto.passport_groups import CreatePassportGroupDTO, UpdatePassportGroupDTO
from core.enums import Permission
from core.exceptions.base import CreateError, UpdateError
from core.passport_groups.entities.passport_group import PassportGroupEntity
from core.services import BaseService


class PassportGroupsServiceImpl(BaseService):

    repository: PassportGroupRepositoryProtocol

    async def get_passport_group_by_name_or_none(self, name: str) -> PassportGroupEntity:
        self.user_entity.check_permission_read_passport_groups()
        return await self.repository.get_passport_group_by_name_or_none(name)

    async def get_passport_group_by_id_or_none(self, _id: int) -> PassportGroupEntity:
        self.user_entity.check_permission_read_passport_groups()
        return await self.repository.get_one_by_id_or_none(_id)

    async def get_all_passport_groups(self) -> Sequence[PassportGroupEntity]:
        self.user_entity.check_permission_read_passport_groups()
        return await self.repository.get_all()

    async def create_passport_group(self, passport_group_dto: CreatePassportGroupDTO) -> PassportGroupEntity:
        self.user_entity.check_permissions(Permission.CREATE_PASSPORT_GROUPS)
        region_entity = PassportGroupEntity(
            group_name=passport_group_dto.group_name,
            group_name_route=passport_group_dto.group_name_route,
            description=passport_group_dto.description,
        )
        passport_group_exists = await self.repository.get_one_or_none_by_filters(
            group_name=passport_group_dto.group_name,
            group_name_route=passport_group_dto.group_name_route,
        )
        if passport_group_exists is not None:
            raise CreateError('Паспортная группа уже существует.')
        return await self.repository.add(region_entity)

    async def update_passport_group(self, passport_group_dto: UpdatePassportGroupDTO) -> PassportGroupEntity:
        self.user_entity.check_permissions(Permission.UPDATE_PASSPORT_GROUPS)
        current_passport_group = await self.repository.get_passport_group_by_name_or_none(passport_group_dto.group_name_to_update)
        if current_passport_group is None:
            raise UpdateError('Паспортная группа с данным названием не найдена.')
        updated_passport_group = PassportGroupEntity(
            id=current_passport_group.id,
            group_name=passport_group_dto.group_name,
            group_name_route=passport_group_dto.group_name_route,
            description=passport_group_dto.description,
        )
        if current_passport_group == updated_passport_group:
            raise UpdateError('Нет отличий в обновляемых полях.')
        update_data_as_dict = {
            k: v for k, v in asdict(passport_group_dto).items() if v is not None
        }
        return await self.repository.update(
            _id=current_passport_group.id,
            **update_data_as_dict,
        )