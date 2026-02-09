from application.base_crud_use_cases import (
    BaseCreateUseCase,
    BaseReadUseCase,
    BaseUpdateUseCase,
    BaseDeleteUseCase,
)
from application.dto.regions import RegionDTO


type RegionCreateUseCase = BaseCreateUseCase[RegionDTO]
type RegionReadUseCase = BaseReadUseCase[RegionDTO]
type RegionUpdateUseCase = BaseUpdateUseCase[RegionDTO]
type RegionDeleteUseCase = BaseDeleteUseCase[RegionDTO]
