from collections.abc import Sequence
from typing import Protocol

from application.interfaces.repositories.passport_groups import PassportGroupRepositoryProtocol
from core.dto.passport_groups import CreatePassportGroupDTO, UpdatePassportGroupDTO
from core.passport_groups.entities.passport_group import PassportGroupEntity
from core.users.entities.user import UserEntity


class PassportGroupsServiceProtocol(Protocol):

    def __init__(
        self,
        user_entity: UserEntity,
        repository: PassportGroupRepositoryProtocol,
    ):
        self.user_entity = user_entity
        self.repository = repository

    async def get_passport_group_by_name_or_none(self, name: str) -> PassportGroupEntity: ...

    async def get_passport_group_by_id_or_none(self, _id: int) -> PassportGroupEntity: ...

    async def get_all_passport_groups(self) -> Sequence[PassportGroupEntity]: ...

    async def create_passport_group(self, passport_group: CreatePassportGroupDTO) -> PassportGroupEntity: ...

    async def update_passport_group(self, passport_group: UpdatePassportGroupDTO) -> PassportGroupEntity: ...


