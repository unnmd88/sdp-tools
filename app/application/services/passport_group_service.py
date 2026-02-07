import logging
from dataclasses import dataclass

from app_logging.dev.config import DOMAIN
from application.utils import async_handle_corrupted_data_in_repo
from domain.cqrs.passport_groups_commands import CreatePassportGroupCommand
from domain.entities.passport_group_entity import PassportGroupEntity
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
    async def get_passport_group_by_name(self, name: str, raise_if_not_found=False) -> PassportGroupEntity | None:
        passport_group = await self.passport_group_repository.get_by_filters({"name": name})
        if passport_group is None and raise_if_not_found:
            raise DomainEntityNotFoundError(
                public_message=f"Группа паспортов с именем={name} не найдена."
            )
        return await self.passport_group_repository.get_by_filters({"name": name})

    async def add_passport_group(self, command: CreatePassportGroupCommand) -> PassportGroupEntity:
        exists_passport_group = await self.get_passport_group_by_name(command.name)
        if exists_passport_group:
            raise DomainEntityAlreadyExistsError(
                public_message=f"Группа паспортов с именем={command.name} уже существует."
            )
        region = PassportGroupEntity.create_new_passport_group(
            name=command.name,
            description=command.description,
        )
        return await self.passport_group_repository.add(region)
