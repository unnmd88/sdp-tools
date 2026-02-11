from collections.abc import Container
from dataclasses import dataclass
from enum import Enum
from typing import Protocol, Self

from application.interfaces import UserServiceProtocol
from application.interfaces.uow_interface import UnitOfWorkProtocol
from domain.kernel.enums.unsorted import Roles


class CommandProtocol(Protocol):
    operation_name: str
    customer_id: int


class MapperToDTOProtocol(Protocol):
    @classmethod
    def from_entity(cls, entity) -> Self: ...


class BaseDeleteProtocol[T_Entity](Protocol):
    async def delete(self, command: CommandProtocol) -> T_Entity: ...


class BaseUpdateProtocol[T_Entity](Protocol):
    async def update(self, command: CommandProtocol) -> T_Entity: ...


class BaseCreateProtocol[T_Entity](Protocol):
    async def create(self, command: CommandProtocol) -> T_Entity: ...


class BaseReadProtocol[T_Entity](Protocol):
    async def get_by_id(self, _id: int) -> T_Entity: ...
    async def get_many(
        self,
        skip: int,
        limit: int,
        order_by: list | None,
    ) -> list[T_Entity]: ...


class DefaultRequireRoles(Enum):
    CREATE = frozenset([Roles.ADMIN, Roles.SUPERUSER, Roles.DIRECTOR])
    UPDATE = frozenset([Roles.SUPERUSER, Roles.DIRECTOR])
    DELETE = frozenset([Roles.SUPERUSER, Roles.DIRECTOR])


@dataclass(frozen=True, slots=True, kw_only=True)
class BaseReadUseCase[T_DTO: MapperToDTOProtocol]:
    entity_service: BaseReadProtocol
    to_dto_mapper: type[MapperToDTOProtocol]

    async def get_by_id(self, _id: int) -> T_DTO:
        entity = await self.entity_service.get_by_id(_id)
        return self.to_dto_mapper.from_entity(entity)

    async def get_many(
        self,
        skip: int = 0,
        limit: int = 100,
        order_by: list | None = None,
    ) -> list[T_DTO]:
        return [
            self.to_dto_mapper.from_entity(region)
            for region in await self.entity_service.get_many(
                skip=skip, limit=limit, order_by=order_by
            )
        ]


@dataclass(frozen=True, slots=True, kw_only=True)
class BaseCreateUseCase[T_DTO: MapperToDTOProtocol]:
    require_roles: Container[Roles] = DefaultRequireRoles.CREATE.value
    uow: UnitOfWorkProtocol
    user_service: UserServiceProtocol
    entity_service: BaseCreateProtocol
    to_dto_mapper: type[MapperToDTOProtocol]

    async def __call__(self, command: CommandProtocol) -> T_DTO:
        async with self.uow:
            await self.user_service.verify_user_is_active_and_has_roles(
                user_id=command.customer_id,
                required_roles=self.require_roles,
                action=command.operation_name,
            )
            entity = await self.entity_service.create(command)
        return self.to_dto_mapper.from_entity(entity)


@dataclass(frozen=True, slots=True, kw_only=True)
class BaseDeleteUseCase[T_DTO: MapperToDTOProtocol]:
    require_roles: Container[Roles] = DefaultRequireRoles.DELETE.value
    uow: UnitOfWorkProtocol
    user_service: UserServiceProtocol
    entity_service: BaseDeleteProtocol
    to_dto_mapper: type[MapperToDTOProtocol]

    async def __call__(self, command: CommandProtocol) -> T_DTO:
        async with self.uow:
            await self.user_service.verify_user_is_active_and_has_roles(
                user_id=command.customer_id,
                required_roles=self.require_roles,
                action=command.operation_name,
            )
            entity = await self.entity_service.delete(command)
        return self.to_dto_mapper.from_entity(entity)


@dataclass(frozen=True, slots=True, kw_only=True)
class BaseUpdateUseCase[T_DTO: MapperToDTOProtocol]:
    require_roles: Container[Roles] = DefaultRequireRoles.UPDATE.value
    uow: UnitOfWorkProtocol
    user_service: UserServiceProtocol
    entity_service: BaseUpdateProtocol
    to_dto_mapper: type[MapperToDTOProtocol]

    async def __call__(self, command: CommandProtocol) -> T_DTO:
        async with self.uow:
            await self.user_service.verify_user_is_active_and_has_roles(
                user_id=command.customer_id,
                required_roles=self.require_roles,
                action=command.operation_name,
            )
            entity = await self.entity_service.update(command)
        return self.to_dto_mapper.from_entity(entity)
