import logging
from dataclasses import dataclass

from app_logging.dev.config import DOMAIN
from application.utils import async_handle_corrupted_data_in_repo
from domain.cqrs.passport_groups_commands import CreatePassportGroupCommand, UpdatePassportGroupCommand, \
    DeletePassportGroupCommand
from domain.entities.passport_group_entity import PassportGroupEntity
from domain.enums.keep_value_enum import Keep
from domain.exceptions import DomainEntityAlreadyExistsError, DomainEntityNotFoundError
from domain.repositories.passport_groups_repo_interface import PassportGroupRepositoryProtocol

logger = logging.getLogger(DOMAIN)


@dataclass(frozen=True, slots=True, kw_only=True)
class PassportGroupServiceImpl:
    passport_group_repository: PassportGroupRepositoryProtocol

    @async_handle_corrupted_data_in_repo(logger=logger)
    async def get_passport_group_by_id(self, _id: int) -> PassportGroupEntity | None:
        return await self.passport_group_repository.get_by_id(_id)

    @async_handle_corrupted_data_in_repo(logger=logger)
    async def get_passport_group_by_name(
        self,
        *,
        name: str,
        raise_if_not_found: bool = False
    ) -> PassportGroupEntity | None:
        passport_group = await self.passport_group_repository.get_by_filters({"name": name})
        if passport_group is None and raise_if_not_found:
            raise DomainEntityNotFoundError(
                public_message=f"Группа паспортов с именем={name} не найдена."
            )
        return await self.passport_group_repository.get_by_filters({"name": name})

    async def get_many(
        self,
        skip: int = 0,
        limit: int | None = None,
        order_by: list | None = None,
        **filters,
    ) -> list[PassportGroupEntity]:
        return await self.passport_group_repository.get_many(
            skip=skip,
            limit=limit,
            order_by=order_by,
            **filters,
        )

    async def add_passport_group(self, command: CreatePassportGroupCommand) -> PassportGroupEntity:
        exists_passport_group = await self.get_passport_group_by_name(name=command.name)
        if exists_passport_group:
            raise DomainEntityAlreadyExistsError(
                public_message=f"Группа паспортов с именем={command.name} уже существует."
            )
        region = PassportGroupEntity.create_new_passport_group(
            name=command.name,
            description=command.description,
        )
        return await self.passport_group_repository.add(region)

    async def update_passport_group(self, command: UpdatePassportGroupCommand) -> PassportGroupEntity:
        passport_group = await self.get_passport_group_by_name(name=command.name, raise_if_not_found=True)
        if command.new_name != Keep.VALUE:
            passport_group.name = command.new_name
        if command.new_description != Keep.VALUE:
            passport_group.description = command.new_description
        return await self.passport_group_repository.update(passport_group)

    async def delete_passport_group(self, command: DeletePassportGroupCommand) -> PassportGroupEntity | None:
        exists_passport_group = await self.get_passport_group_by_name(
            name=command.name, raise_if_not_found=True
        )
        return await self.passport_group_repository.delete(exists_passport_group.id)