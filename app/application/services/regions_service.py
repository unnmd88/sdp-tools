import logging
from dataclasses import dataclass

from app_logging.dev.config import DOMAIN
from application.helpers.entity_fetcher import EntityFetcher
from application.utils import async_handle_corrupted_data_in_repo
from domain.cqrs.region_commands import (
    UpdateRegionCommand,
    CreateRegionCommand,
    DeleteRegionCommand,
)
from domain.entities.region_entity import RegionEntity
from domain.enums.keep_value_enum import Keep
from domain.exceptions import (
    DomainEntityNotFoundError,
    DomainEntityAlreadyExistsError,
    DomainValidationError,
)
from domain.repositories.regions_repo_interface import RegionsRepositoryProtocol

logger = logging.getLogger(DOMAIN)


@dataclass(frozen=True, slots=True, kw_only=True)
class RegionsServiceImpl:
    repository: RegionsRepositoryProtocol
    fetcher: EntityFetcher[RegionEntity] = EntityFetcher(
        user_friendly_entity_name="Регионы"
    )

    def _check_and_build_criteria_for_search_by_code_or_name(
        self, code_or_name: int | str
    ) -> dict[str, int | str]:
        if isinstance(code_or_name, int) or code_or_name.isdigit():
            code_or_name = int(code_or_name)
            return {"code": code_or_name}
        elif isinstance(code_or_name, str):
            return {"name": code_or_name}
        else:
            raise DomainValidationError(
                private_message=f"Неверный тип данных для поиска региона. code_or_name={code_or_name}",
                public_message=f"Неверный тип данных для поиска региона. Ожидается строка или число.",
            )

    async def get_by_id(self, region_id: int) -> RegionEntity:
        return await self.fetcher.fetch(
            fetch_method=self.repository.get_by_id,
            identifier=region_id,
            identifier_label="ID",
            raise_if_not_found=True,
        )

    async def try_by_id(self, region_id: int) -> RegionEntity | None:
        return await self.fetcher.fetch(
            fetch_method=self.repository.get_by_id,
            identifier=region_id,
            identifier_label="ID",
        )

    async def get_by_code_or_name(self, code_or_name: int | str) -> RegionEntity:
        return await self.fetcher.fetch(
            fetch_method=self.repository.get_by_filters,
            identifier=self._check_and_build_criteria_for_search_by_code_or_name(
                code_or_name
            ),
            raise_if_not_found=True,
        )

    async def try_by_code_or_name(self, code_or_name: int | str) -> RegionEntity:
        return await self.fetcher.fetch(
            fetch_method=self.repository.get_by_filters,
            identifier=self._check_and_build_criteria_for_search_by_code_or_name(
                code_or_name
            ),
            raise_if_not_found=False,
        )

    @async_handle_corrupted_data_in_repo(logger=logger)
    async def get_many(
        self,
        skip: int = 0,
        limit: int | None = None,
        order_by: list | None = None,
        **filters,
    ) -> list[RegionEntity]:
        return await self.repository.get_many(
            skip=skip,
            limit=limit,
            order_by=order_by,
            **filters,
        )

    async def create(self, command: CreateRegionCommand) -> RegionEntity:
        exists_region = await self.try_by_code_or_name(code_or_name=command.name)
        if exists_region:
            raise DomainEntityAlreadyExistsError(
                public_message=f"Регион с именем={command.name} уже существует."
            )
        exists_region = await self.try_by_code_or_name(code_or_name=command.code)
        if exists_region:
            raise DomainEntityAlreadyExistsError(
                public_message=f"Регион с кодом={command.code} уже существует."
            )
        region = RegionEntity.create_new_region(
            code=command.code,
            name=command.name,
        )
        return await self.repository.add(region)

    async def update(self, command: UpdateRegionCommand) -> RegionEntity:
        region = await self.get_by_code_or_name(code_or_name=command.code_or_name)
        if command.new_code != Keep.VALUE:
            region.code = command.new_code
        if command.new_name != Keep.VALUE:
            region.name = command.new_name
        return await self.repository.update(region)

    async def delete(self, command: DeleteRegionCommand) -> RegionEntity | None:
        exists_region = await self.get_by_code_or_name(
            code_or_name=command.code_or_name
        )
        return await self.repository.delete(exists_region.id)
