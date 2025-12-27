from collections.abc import Sequence
from dataclasses import asdict

from application.interfaces.repositories.regions import RegionsRepositoryProtocol
from core.dto.regions import RegionsDTO, UpdateRegionsDTO
from core.enums import Permissions
from core.exceptions.base import CreateError, UpdateError
from core.regions.entities.region import RegionEntity
from core.services import BaseService
from core.users.exceptions import DomainValidationError


class RegionsServiceImpl(BaseService):

    repository: RegionsRepositoryProtocol

    async def get_region_by_name_or_none(self, name: str) -> RegionEntity:
        self.user_entity.check_permission_read_region()
        return await self.repository.get_region_by_name_or_none(name)

    async def get_region_by_code_or_none(self, region_code: int) -> RegionEntity:
        self.user_entity.check_permission_read_region()
        return await self.repository.get_region_by_code_or_none(region_code)

    async def get_region_by_id_or_none(self, _id: int) -> RegionEntity:
        self.user_entity.check_permission_read_region()
        return await self.repository.get_one_by_id_or_none(_id)

    async def get_all_regions(self) -> Sequence[RegionEntity]:
        self.user_entity.check_permission_read_region()
        return await self.repository.get_all()

    async def create_region(self, region: RegionsDTO) -> RegionEntity:
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
        return await self.repository.add(region_entity)

    async def update_region(self, region: UpdateRegionsDTO) -> RegionEntity:
        self.user_entity.check_permissions(Permissions.UPDATE_REGIONS)
        current_region = await self.repository.get_region_by_name_or_none(region.region_name_to_update)
        if current_region is None:
            raise UpdateError('Регион с данным названием не найден.')
        updated_region = RegionEntity(
            id=current_region.id,
            code=region.code or current_region.code,
            name=region.name or current_region.name,
        )
        if current_region == updated_region:
            raise UpdateError('Нет отличий в обновляемых полях.')
        update_data_as_dict = {
            k: v for k, v in asdict(region).items() if v is not None
        }
        return await self.repository.update(
            _id=current_region.id,
            **update_data_as_dict,
        )