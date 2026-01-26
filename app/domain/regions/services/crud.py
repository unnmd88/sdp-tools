import logging
from collections.abc import Sequence

from app_logging.dev.config import COMMON_LOGGER
from application.interfaces.repositories.regions import RegionsRepositoryProtocol
from domain.dto.common import (
    FiltersForSearchDTO,
    CreateRecordDTO,
    UpdatedRecordDTO,
    ToUpdateRecordDTO,
)
from domain.enums import Permissions
from domain._exceptions.base import DomainValidationError
from domain._exceptions.crud import CreateError, CreateErrorAlreadyExists, UpdateError
from domain.regions.entities.region import RegionEntity


logger = logging.getLogger(COMMON_LOGGER)


class RegionsServiceImpl:
    repository: RegionsRepositoryProtocol

    async def get_region_by_id_or_none(self, _id: int) -> RegionEntity:
        self.user_entity.access_control_read_region()
        return await self.repository.get_one_by_id_or_none(_id)

    async def get_region_by_filters_or_none(
        self, filters_dto: FiltersForSearchDTO
    ) -> RegionEntity | None:
        self.user_entity.access_control_read_region()
        return await self.repository.get_one_or_none_by_filters(
            filters_dto.search_filters
        )

    async def get_all_regions(self) -> Sequence[RegionEntity]:
        self.user_entity.access_control_read_region()
        return await self.repository.get_many()

    async def create_region(self, create_dto: CreateRecordDTO) -> RegionEntity:
        self.user_entity.access_control(Permissions.CREATE_REGIONS)
        logger.info(
            "Юзер %r: запрос на создание нового региона: %r",
            self.user_entity.username_length,
            create_dto.fields,
        )
        try:
            new_region_entity = await self.repository.add(create_dto)
        except DomainValidationError:
            logger.info(
                "Некорректные данные для создания региона: %r", create_dto.fields
            )
            raise
        except CreateErrorAlreadyExists:
            logger.info("Регион уже существует")
            raise
        except CreateError:
            logger.error("Ошибка создания региона: %r", create_dto.fields)
            raise
        logger.info("Новый регион успешно создан: %r", new_region_entity)
        return new_region_entity

    async def update_region(self, update_dto: ToUpdateRecordDTO) -> UpdatedRecordDTO:
        self.user_entity.access_control(Permissions.UPDATE_REGIONS)
        logger.info(
            "Юзер %r: запрос на обновление региона %r\nДанные для обновления: %r",
            self.user_entity.username_length,
            update_dto.search_criteria,
            update_dto.fields,
        )
        try:
            update_dto = await self.repository.update_one(update_dto)
        except UpdateError as e:
            logger.error("Ошибка обновления данных: %r", e)
            raise UpdateError
        logger.info(
            "Регион обновлён.\nСтарые значения: %r\nНовые значения:  %r",
            update_dto.old,
            update_dto.new,
        )
        return update_dto

    async def delete_region(self, filters_dto: FiltersForSearchDTO) -> RegionEntity:
        self.user_entity.access_control(Permissions.DELETE_REGIONS)
        logger.info(
            "Юзер %r: запрос на удаление региона: %r",
            self.user_entity.username_length,
            filters_dto.search_filters,
        )
        try:
            entity = await self.repository.delete_one(filters_dto)
        except UpdateError as e:
            logger.info("Ошибка удаления: %r", e)
            raise UpdateError
        logger.info("Регион удалён: %r", entity)
        return entity
