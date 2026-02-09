from application.base_crud_use_cases import (
    BaseCreateUseCase,
    BaseReadUseCase,
    BaseUpdateUseCase,
    BaseDeleteUseCase,
)
from application.dto.passport_groups import PassportGroupDTO

type PassportGroupCreateUseCase = BaseCreateUseCase[PassportGroupDTO]
type PassportGroupReadUseCase = BaseReadUseCase[PassportGroupDTO]
type PassportGroupUpdateUseCase = BaseUpdateUseCase[PassportGroupDTO]
type PassportGroupDeleteUseCase = BaseDeleteUseCase[PassportGroupDTO]
