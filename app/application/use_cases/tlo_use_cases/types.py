from application.base_crud_use_cases import BaseCreateUseCase, BaseReadUseCase
from application.dto.tlo_dto import TrafficLightObjectDTO

type TrafficLightObjectsCreateUseCase = BaseCreateUseCase[TrafficLightObjectDTO]
type TrafficLightObjectsReadUseCase = BaseReadUseCase[TrafficLightObjectDTO]
# type TrafficLightObjectsUpdateUseCase = BaseUpdateUseCase[RegionDTO]
# type TrafficLightObjectsDeleteUseCase = BaseDeleteUseCase[RegionDTO]