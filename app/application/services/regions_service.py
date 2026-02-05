import logging
from collections.abc import Sequence
from dataclasses import dataclass

from app_logging.dev.config import DOMAIN
from application.exceptions import InactiveAccountError
from application.utils import async_handle_corrupted_data_in_repo
from domain.entities.region_entity import RegionEntity
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
    async def get_region_by_filters(self, **filters) -> RegionEntity | None:
        return await self.regions_repository.get_by_filters(**filters)

    async def get_region_by_code(self, code: int) -> RegionEntity | None:
        return await self.regions_repository.get_by_code(code)

    async def get_region_by_name(self, name: str) -> RegionEntity | None:
        return await self.regions_repository.get_by_name(name)

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
