import logging
from dataclasses import dataclass
from typing import final

from app_logging.dev.config import DOMAIN
from application.helpers.entity_fetcher import EntityFetcher
from application.utils import async_handle_corrupted_data_in_repo
from domain.cqrs.passport_groups_commands import (
    CreatePassportGroupCommand,
    UpdatePassportGroupCommand,
    DeletePassportGroupCommand,
)

from domain.entities.passport_group_entity import PassportGroupEntity
from domain.enums.keep_value_enum import Keep
from domain.exceptions import DomainEntityAlreadyExistsError
from domain.repositories.passport_groups_repo_interface import (
    PassportGroupRepositoryProtocol,
)

logger = logging.getLogger(DOMAIN)


@final
@dataclass(slots=True, kw_only=True, frozen=True)
class PassportGroupServiceImpl:
    repository: PassportGroupRepositoryProtocol
    fetcher: EntityFetcher[PassportGroupEntity] = EntityFetcher(
        user_friendly_entity_name="Группа паспортов"
    )

    async def get_by_id(self, passport_group_id: int) -> PassportGroupEntity:
        return await self.fetcher.fetch(
            fetch_method=self.repository.get_by_id,
            identifier=passport_group_id,
            identifier_label="ID",
            raise_if_not_found=True,
        )

    async def try_by_id(self, passport_group_id: int) -> PassportGroupEntity | None:
        return await self.fetcher.fetch(
            fetch_method=self.repository.get_by_id,
            identifier=passport_group_id,
            identifier_label="ID",
        )

    async def get_by_name(self, passport_group_name: str) -> PassportGroupEntity:
        return await self.fetcher.fetch(
            fetch_method=self.repository.get_by_filters,
            identifier={"name": passport_group_name},
            identifier_label="name",
            raise_if_not_found=True,
        )

    async def try_by_name(self, passport_group_name: str) -> PassportGroupEntity | None:
        return await self.fetcher.fetch(
            fetch_method=self.repository.get_by_filters,
            identifier={"name": passport_group_name},
            identifier_label="name",
            raise_if_not_found=False,
        )

    @async_handle_corrupted_data_in_repo(logger=logger)
    async def get_many(
        self,
        skip: int = 0,
        limit: int | None = None,
        order_by: list | None = None,
        **filters,
    ) -> list[PassportGroupEntity]:
        return await self.repository.get_many(
            skip=skip,
            limit=limit,
            order_by=order_by,
            **filters,
        )

    async def create(self, command: CreatePassportGroupCommand) -> PassportGroupEntity:
        exists_passport_group = await self.try_by_name(passport_group_name=command.name)
        if exists_passport_group:
            raise DomainEntityAlreadyExistsError(
                public_message=f"Группа паспортов с именем={command.name} уже существует."
            )
        region = PassportGroupEntity.create_new_passport_group(
            name=command.name,
            description=command.description,
        )
        return await self.repository.add(region)

    async def update(self, command: UpdatePassportGroupCommand) -> PassportGroupEntity:
        exists_passport_group = await self.get_by_name(passport_group_name=command.name)
        if command.new_name != Keep.VALUE:
            exists_passport_group.name = command.new_name
        if command.new_description != Keep.VALUE:
            exists_passport_group.description = command.new_description
        return await self.repository.update(exists_passport_group)

    async def delete(self, command: DeletePassportGroupCommand) -> PassportGroupEntity:
        exists_passport_group = await self.get_by_name(passport_group_name=command.name)
        return await self.repository.delete(exists_passport_group.id)
