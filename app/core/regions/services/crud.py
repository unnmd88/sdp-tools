import logging
from collections.abc import Sequence
from dataclasses import asdict

from app_logging.dev.config import COMMON_LOGGER
from application.interfaces.repositories.regions import RegionsRepositoryProtocol
from core.dto.filters import FiltersForSearchDTO
from core.dto.regions import UpdateRegionDTO, CreateRegionDTO
from core.dto.update_entity import UpdatedEntityDTO
from core.enums import Permissions
from core.exceptions.base import CreateError, UpdateError
from core.regions.entities.region import RegionEntity
from core.services import BaseService
from core.utils import not_none_dataclass_instance_attrs_to_dict

logger = logging.getLogger(COMMON_LOGGER)


class RegionsServiceImpl(BaseService):

    repository: RegionsRepositoryProtocol

    async def get_region_by_id_or_none(self, _id: int) -> RegionEntity:
        self.user_entity.check_permission_read_region()
        return await self.repository.get_one_by_id_or_none(_id)

    async def get_region_by_filters_or_none(self, filters_dto: FiltersForSearchDTO) -> RegionEntity | None:
        self.user_entity.check_permission_read_region()
        return await self.repository.get_one_or_none_by_filters(
            **filters_dto.filters_for_search
        )

    async def get_all_regions(self) -> Sequence[RegionEntity]:
        self.user_entity.check_permission_read_region()
        return await self.repository.get_all()

    async def create_region(self, region: CreateRegionDTO) -> RegionEntity:
        self.user_entity.check_permissions(Permissions.CREATE_REGIONS)
        region_entity = RegionEntity(
            name=region.name,
            code=region.code,
        )
        region_exists = await self.repository.get_one_or_none_by_filters(
            name=region_entity.name,
            code=region_entity.code
        )
        if region_exists is not None:
            raise CreateError('Регион уже существует.')
        new_entity = await self.repository.add(region_entity)
        logger.info('Пользователь %r добавил новый регион: %r', self.user_entity.username, new_entity)
        return new_entity

    async def update_region(self, region: UpdateRegionDTO) -> UpdatedEntityDTO:
        self.user_entity.check_permissions(Permissions.UPDATE_REGIONS)
        logger.info(
            'Юзер %r: запрос на обновление региона %r\nДанные для обновления: %r',
            self.user_entity.username, region.code_or_name, region
        )
        try:
            update_dto = await self.repository.update_one(
                region.filters_for_search,
                **not_none_dataclass_instance_attrs_to_dict(region, 'code_or_name'),
            )
        except UpdateError as e:
            logger.error('Ошибка обновления данных: %r', e)
            raise UpdateError
        logger.info(
            'Регион обновлён.\nСтарые значения: %r\nНовые значения:  %r',
            update_dto.old, update_dto.new
        )
        return update_dto

    async def delete_region(self, _id: int) -> RegionEntity:
        self.user_entity.check_permissions(Permissions.DELETE_REGIONS)
        logger.info(
            'Юзер %r: запрос на удаление региона с id=%r',
            self.user_entity.username, _id,
        )
        try:
            entity = await self.repository.delete_one(_id)
        except UpdateError as e:
            logger.info('Ошибка удаления: %r', e)
            raise UpdateError
        logger.info( 'Регион удалён: %r',entity)
        return entity