from typing import Protocol

from domain.cqrs.passport_groups_commands import (
    UpdatePassportGroupCommand,
    CreatePassportGroupCommand,
    DeletePassportGroupCommand,
)
from domain.entities.passport_group_entity import PassportGroupEntity


class PassportGroupReadServiceProtocol(Protocol):
    async def get_by_id(self, _id: int) -> PassportGroupEntity: ...
    async def get_by_name(self, name: str) -> PassportGroupEntity: ...
    async def get_many(
        self,
        skip: int,
        limit: int,
        order_by: list | None,
    ) -> list[PassportGroupEntity]: ...


class PassportGroupWriteServiceProtocol(Protocol):
    async def update(
        self, command: UpdatePassportGroupCommand
    ) -> PassportGroupEntity: ...
    async def create(
        self, command: CreatePassportGroupCommand
    ) -> PassportGroupEntity: ...
    async def delete(
        self, command: DeletePassportGroupCommand
    ) -> PassportGroupEntity: ...


class PassportGroupServiceProtocol(
    PassportGroupReadServiceProtocol, PassportGroupWriteServiceProtocol, Protocol
): ...
