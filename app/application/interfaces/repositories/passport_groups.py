from collections.abc import Sequence

from application.interfaces.repositories.base import BaseCrudProtocol
from core.dto.passport_groups import CreatePassportGroupsDTO, UpdatePassportGroupsDTO
from core.passport_groups.entities.passport_group import PassportGroupEntity


class PassportGroupRepositoryProtocol(BaseCrudProtocol):

    async def get_passport_group_by_name_or_none(self, name: str) -> PassportGroupEntity | None: ...

    async def get_passport_group_by_id_or_none(self, _id: int) -> PassportGroupEntity: ...

    async def get_all_passport_groups(self) -> Sequence[PassportGroupEntity]: ...

    async def create_region(self, region: CreatePassportGroupsDTO) -> PassportGroupEntity: ...

    async def update_region(self, user: UpdatePassportGroupsDTO) -> PassportGroupEntity: ...
