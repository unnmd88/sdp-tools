from collections.abc import Sequence

from application.interfaces.repositories.passport_groups import (
    PassportGroupRepositoryProtocol,
)
from domain.dto.passport_groups import CreatePassportGroupDTO, UpdatePassportGroupDTO
from domain.enums import Permissions
from domain.exceptions.crud import CreateError, UpdateError
from domain.passport_groups.entities.passport_group import PassportGroupEntity
from domain.utils import not_none_dataclass_instance_attrs_to_dict


class PassportGroupsServiceImpl:
    repository: PassportGroupRepositoryProtocol

    async def get_passport_group_by_name_or_none(
        self, name: str
    ) -> PassportGroupEntity:
        self.user_entity.access_control_read_passport_groups()
        return await self.repository.get_passport_group_by_name_or_none(name)

    async def get_passport_group_by_id_or_none(self, _id: int) -> PassportGroupEntity:
        self.user_entity.access_control_read_passport_groups()
        return await self.repository.get_one_by_id_or_none(_id)

    async def get_all_passport_groups(self) -> Sequence[PassportGroupEntity]:
        self.user_entity.access_control_read_passport_groups()
        return await self.repository.get_all()

    async def create_passport_group(
        self, passport_group_dto: CreatePassportGroupDTO
    ) -> PassportGroupEntity:
        self.user_entity.access_control(Permissions.CREATE_PASSPORT_GROUPS)
        passport_group_entity = PassportGroupEntity(
            group_name=passport_group_dto.group_name,
            description=passport_group_dto.description,
        )
        passport_group_exists = await self.repository.get_one_or_none_by_filters(
            group_name=passport_group_dto.group_name,
        )
        if passport_group_exists is not None:
            raise CreateError("Паспортная группа уже существует.")
        return await self.repository.add(passport_group_entity)

    async def update_passport_group(
        self, passport_group_dto: UpdatePassportGroupDTO
    ) -> PassportGroupEntity:
        self.user_entity.access_control(Permissions.UPDATE_PASSPORT_GROUPS)
        current_passport_group = (
            await self.repository.get_passport_group_by_name_or_none(
                passport_group_dto.group_name_to_update
            )
        )
        if current_passport_group is None:
            raise UpdateError("Паспортная группа с данным названием не найдена.")
        updated_passport_group = PassportGroupEntity(
            id=current_passport_group.id,
            group_name=passport_group_dto.group_name,
            description=passport_group_dto.description,
        )
        if current_passport_group == updated_passport_group:
            raise UpdateError("Нет отличий в обновляемых полях.")

        return await self.repository.update(
            _id=current_passport_group.id,
            **not_none_dataclass_instance_attrs_to_dict(passport_group_dto),
        )
