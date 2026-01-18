from collections.abc import Sequence

from application.interfaces.repositories.base_repo_interface import BaseCrudProtocol
from domain.dto.passport_groups import CreatePassportGroupDTO, UpdatePassportGroupDTO
from domain.passport_groups.entities.passport_group import PassportGroupEntity


class PassportGroupRepositoryProtocol(BaseCrudProtocol):
    async def get_passport_group_by_name_or_none(
        self, name: str
    ) -> PassportGroupEntity | None: ...

    async def get_passport_group_by_id_or_none(
        self, _id: int
    ) -> PassportGroupEntity: ...

    async def get_all_passport_groups(self) -> Sequence[PassportGroupEntity]: ...

    async def create_region(
        self, region: CreatePassportGroupDTO
    ) -> PassportGroupEntity: ...

    async def update_region(
        self, user: UpdatePassportGroupDTO
    ) -> PassportGroupEntity: ...
