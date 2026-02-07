from typing import Protocol, Any

from domain.cqrs.passport_groups_commands import (
    UpdatePassportGroupCommand,
    CreatePassportGroupCommand,
    DeletePassportGroupCommand,
)
from domain.entities.passport_group_entity import PassportGroupEntity


class PassportGroupReadServiceProtocol(Protocol):
    async def get_passport_group_by_and_filters(self, **filters) -> PassportGroupEntity | None: ...
    async def get_passport_group_by_id(self, id: int) -> PassportGroupEntity | None: ...
    async def get_passport_group_by_name(
        self,
        *,
        name: str,
        raise_if_not_found: bool,
    ) -> PassportGroupEntity | None: ...
    async def get_passport_group_by_id_or_raise(self, _id: int) -> PassportGroupEntity: ...
    async def get_many(
        self,
        skip: int,
        limit: int,
        order_by: list | None,
    ) -> list[PassportGroupEntity]: ...


class PassportGroupWriteServiceProtocol(Protocol):
    async def update_passport_group(self, command: UpdatePassportGroupCommand) -> PassportGroupEntity: ...
    async def add_passport_group(self, command: CreatePassportGroupCommand) -> PassportGroupEntity: ...
    async def delete_passport_group(self, command: DeletePassportGroupCommand) -> PassportGroupEntity | None: ...


class PassportGroupServiceProtocol(
    PassportGroupReadServiceProtocol, PassportGroupWriteServiceProtocol, Protocol
): ...