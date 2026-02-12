import logging
from dataclasses import dataclass

from app_logging.dev.config import DOMAIN
from application.helpers.entity_fetcher import EntityFetcher
from application.utils import async_handle_corrupted_data_in_repo
from domain.kernel.enums.keep_value_enum import Keep
from domain.regions.region_commands import (
    UpdateRegionCommand,
    CreateRegionCommand,
    DeleteRegionCommand,
)
from domain.exceptions import (
    DomainEntityAlreadyExistsError,
    DomainValidationError,
)
from domain.repositories.tlo_repo_interface import TrafficLightObjectRepositoryProtocol
from domain.traffic_light_objects.tlo_commands import CreateTrafficLightObjectCommand
from domain.traffic_light_objects.tlo_entity import TrafficLightObjectEntity

logger = logging.getLogger(DOMAIN)


@dataclass(frozen=True, slots=True, kw_only=True)
class TrafficLightObjectServiceImpl:
    repository: TrafficLightObjectRepositoryProtocol
    fetcher: EntityFetcher[TrafficLightObjectEntity] = EntityFetcher(
        user_friendly_entity_name="Светофорные объекты"
    )

    # def _check_and_build_criteria_for_search_by_code_or_name(
    #     self, code_or_name: int | str
    # ) -> dict[str, int | str]:
    #     if isinstance(code_or_name, int) or code_or_name.isdigit():
    #         code_or_name = int(code_or_name)
    #         return {"code": code_or_name}
    #     elif isinstance(code_or_name, str):
    #         return {"name": code_or_name}
    #     else:
    #         raise DomainValidationError(
    #             private_message=f"Неверный тип данных для поиска региона. code_or_name={code_or_name}",
    #             public_message=f"Неверный тип данных для поиска региона. Ожидается строка или число.",
    #         )

    async def get_by_id(self, tlo_id: int) -> TrafficLightObjectEntity:
        return await self.fetcher.fetch(
            fetch_method=self.repository.try_by_id,
            identifier=tlo_id,
            identifier_label="ID",
            raise_if_not_found=True,
        )

    async def try_by_id(self, tlo_id: int) -> TrafficLightObjectEntity | None:
        return await self.fetcher.fetch(
            fetch_method=self.repository.try_by_id,
            identifier=tlo_id,
            identifier_label="ID",
        )

    async def get_by_name(self, name: str) -> TrafficLightObjectEntity:
        return await self.fetcher.fetch(
            fetch_method=self.repository.try_by_filters,
            identifier={"name": name},
            raise_if_not_found=True,
        )

    async def try_by_name(self, name: str) -> TrafficLightObjectEntity:
        return await self.fetcher.fetch(
            fetch_method=self.repository.try_by_filters,
            identifier={"name": name},
            raise_if_not_found=False,
        )

    @async_handle_corrupted_data_in_repo(logger=logger)
    async def get_many(
        self,
        skip: int = 0,
        limit: int | None = None,
        order_by: list | None = None,
        **filters,
    ) -> list[TrafficLightObjectEntity]:
        return await self.repository.get_many(
            skip=skip,
            limit=limit,
            order_by=order_by,
            **filters,
        )

    async def create(self, command: CreateTrafficLightObjectCommand) -> TrafficLightObjectEntity:
        exists_region = await self.try_by_name(name=command.name)
        if exists_region:
            raise DomainEntityAlreadyExistsError(
                public_message=f"Светофорный объект с именем {command.name!r} уже существует."
            )
        tlo = TrafficLightObjectEntity.create_new(
            region_id=command.region_id,
            name=command.name,
            traffic_controller_type=command.traffic_controller_type,
            address=command.address,
            created_by_user_id=command.created_by_user_id,
            updated_by_user_id=command.updated_by_user_id,
            latitude=command.latitude,
            longitude=command.longitude,
            district=command.district,
            note=command.note,
        )
        return await self.repository.create(tlo)

    # async def update(self, command: UpdateRegionCommand) -> RegionEntity:
    #     region = await self.get_by_code_or_name(code_or_name=command.code_or_name)
    #     if command.new_code != Keep.VALUE:
    #         region.code = command.new_code
    #     if command.new_name != Keep.VALUE:
    #         region.name = command.new_name
    #     return await self.repository.update(region)
    #
    # async def delete(self, command: DeleteRegionCommand) -> RegionEntity | None:
    #     exists_region = await self.get_by_code_or_name(
    #         code_or_name=command.code_or_name
    #     )
    #     return await self.repository.delete(exists_region.id)

