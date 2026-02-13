from application.base_crud_use_cases import (
    BaseCreateUseCase,
    BaseReadUseCase,
    BaseUpdateUseCase,
    BaseDeleteUseCase,
)
from application.dtos.regions_dto import RegionDTO


type RegionCreateUseCase = BaseCreateUseCase[RegionDTO]
type RegionReadUseCase = BaseReadUseCase[RegionDTO]
type RegionUpdateUseCase = BaseUpdateUseCase[RegionDTO]
type RegionDeleteUseCase = BaseDeleteUseCase[RegionDTO]
