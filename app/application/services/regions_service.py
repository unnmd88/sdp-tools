import logging
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, TypedDict

from app_logging.dev.config import DOMAIN
from application.exceptions import InactiveAccountError
from application.utils import async_handle_corrupted_data_in_repo
from domain.cqrs.region_commands import UpdateRegionCommand
from domain.entities.region_entity import RegionEntity
from domain.enums.keep_value_enum import Keep
from domain.exceptions import DomainEntityNotFoundError
from domain.repositories.regions_repo_interface import RegionsRepositoryProtocol

logger = logging.getLogger(DOMAIN)


@dataclass(frozen=True, slots=True, kw_only=True)
class RegionsServiceImpl:

    regions_repository: RegionsRepositoryProtocol

    @async_handle_corrupted_data_in_repo(logger=logger)
    async def get_region_by_id(self, _id: int) -> RegionEntity | None:
        return await self.regions_repository.get_by_id(_id)

    async def get_region_by_id_or_raise(self, _id: int) -> RegionEntity:
        if (user := await self.get_region_by_id(_id)) is None:
            raise DomainEntityNotFoundError(public_message=f"Регион не найден.")
        return user

    @async_handle_corrupted_data_in_repo(logger=logger)
    async def get_region_by_filters(self, filters: dict) -> RegionEntity | None:
        return await self.regions_repository.get_by_filters(filters)

    async def get_region_by_code_or_name(
        self,
        *,
        code_or_name: str | int,
        raise_if_not_found: bool = False,
    ) -> RegionEntity | None:
        code_or_name = int(code_or_name) if code_or_name.isdigit() else code_or_name
        if isinstance(code_or_name, int):
            region = await self.get_region_by_filters({"code": code_or_name})
        else:
            region = await self.get_region_by_filters({"name": code_or_name})
        if region is None and raise_if_not_found:
            if isinstance(code_or_name, int):
                message = f"Регион с кодом={code_or_name} не найден."
            else:
                message = f"Регион с именем={code_or_name} не найден."
            raise DomainEntityNotFoundError(public_message=message)
        return region

    # async def get_region_by_code(self, code: int) -> RegionEntity | None:
    #     return await self.regions_repository.get_by_code(code)
    #
    # async def get_region_by_name(self, name: str) -> RegionEntity | None:
    #     return await self.regions_repository.get_by_name(name)

    async def get_many(
        self,
        skip: int = 0,
        limit: int | None = None,
        order_by: list | None = None,
        **filters
    ) -> list[RegionEntity]:
        return await self.regions_repository.get_many(
            skip=skip,
            limit=limit,
            order_by=order_by,
            **filters,
        )

    async def update_region(self, command: UpdateRegionCommand) -> RegionEntity:
        region = await self.get_region_by_code_or_name(code_or_name=command.code_or_name, raise_if_not_found=True)
        if command.new_code != Keep.VALUE:
            print("POINT 1")
            region.code = command.new_code
        if command.new_name != Keep.VALUE:
            print("POINT 2")
            region.name = command.new_name
        return region
        return await self.regions_repository.update(region)
