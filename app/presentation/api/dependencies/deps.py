from typing import Annotated

from fastapi import Depends
from fastapi.params import Form

from application.jwt_utils import ManagerJWT
from application.use_cases.auth_jwt_use_case import AuthAndJWTUseCaseImpl
from application.use_cases.passport_groups.crud import PassportGroupsCrudUseCaseImpl
from application.use_cases.regions.crud import RegionsCrudUseCaseImpl
from application.use_cases.users.main_users_use_case import UsersCrudUseCaseImpl
from core.tlo.services.main_tlo_service import TrafficLightObjectServiceImpl
from core.users.entities.user import UserEntity
from presentation.api.dependencies.dependencies import (
    users_use_case,
    get_access_jwt_payload_schema,
    get_regions_crud_use_case,
    is_superuser,
    is_admin,
    get_user_entity_by_id,
    get_passport_groups_use_case,
    get_tlo_use_case,
    get_refresh_jwt_payload_schema, get_auth_and_jwt_use_case,
)
from presentation.api.dependencies.utils import get_filters_for_region_or_name_search
from presentation.schemas.auth import AuthSchema
from presentation.schemas.jwt import PayloadAccessJWTSchema, TokenInfo, PayloadRefreshJWTSchema


def auth_form(
    username: str = Form(),
    password: str = Form(),
):
    return AuthSchema(username=username, password=password)

## Auth
AuthForm = Annotated[AuthSchema, Depends(auth_form)]
AccessAndRefreshJWT = Annotated[TokenInfo, Depends()]
AuthAndJWTUseCase = Annotated[AuthAndJWTUseCaseImpl, Depends(get_auth_and_jwt_use_case)]
ManagerJWTDep = Annotated[ManagerJWT, Depends(ManagerJWT)]
# PayloadJWTDependency = Annotated[PayloadAccessJWTSchema, Depends(get_access_jwt_payload_schema)]
PayloadAccessJWT = Annotated[PayloadAccessJWTSchema, Depends(get_access_jwt_payload_schema)]
PayloadRefreshJWT = Annotated[PayloadRefreshJWTSchema, Depends(get_refresh_jwt_payload_schema)]
IsSuperuser = Depends(is_superuser)
IsAdmin = Depends(is_admin)
# TO DO  AccessFromRefreshJWT = Annotated[TokenInfo, Depends(auth_user_and_issue_access_and_refresh_jwt)]


## Users
UsersUseCase = Annotated[UsersCrudUseCaseImpl, Depends(users_use_case)]
UserEntityDep = Annotated[UserEntity, Depends(get_user_entity_by_id)]

## Regions
RegionsCrudUseCase = Annotated[RegionsCrudUseCaseImpl, Depends(get_regions_crud_use_case)]
regions_filters_for_search = Annotated[int | str, Depends(get_filters_for_region_or_name_search)]
## PassportGroups
PassportGroupsCrudUseCase = Annotated[PassportGroupsCrudUseCaseImpl, Depends(get_passport_groups_use_case)]

## TrafficLightObjects
TrafficLightObjectUseCase = Annotated[TrafficLightObjectServiceImpl, Depends(get_tlo_use_case)]
