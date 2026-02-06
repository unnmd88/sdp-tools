from typing import Annotated

from fastapi import Depends
from fastapi.params import Form

from application.dto.jwt_dto import AccessJWTPayloadDTO
from application.use_cases.admin import create_user_use_case
from application.use_cases.admin.change_password_use_case import ResetUserPasswordByAdminUseCaseImpl
from application.use_cases.regions.read_region_use_case import ReadRegionUseCaseImpl
from application.use_cases.regions.update_regions_use_case import UpdateRegionUseCaseImpl
from application.use_cases.users.change_password_use_case import ChangeUserPasswordUseCaseImpl
from application.use_cases.admin.create_user_use_case import CreateUserUseCaseImpl
from application.use_cases.users.refresh_jwt_use_case import RefreshJWTUseCaseImpl
from application.use_cases.users.user_login_and_issue_jwt_use_case import (
    UserLoginAndIssueJWTUseCaseImpl,
)
from domain.enums.unsorted import TokenTypesEnum

from presentation.api.dependencies.di import (
    get_auth_and_jwt_use_case,
    get_refresh_jwt_use_case,
    get_change_password_use_case, jwt_decoder_factory, get_reset_password_by_admin_use_case, get_create_user_use_case,
    get_read_region_use_case, get_update_region_use_case,
)
from presentation.api.dependencies.utils import get_filters_for_region_or_name_search
from presentation.schemas.auth import AuthSchema


def auth_form(
    username: str = Form(),
    password: str = Form(),
):
    return AuthSchema(username=username, password=password)


## Auth and JWT

AuthForm = Annotated[AuthSchema, Depends(auth_form)]
AccessTokenDep = Annotated[
    AccessJWTPayloadDTO,
    Depends(jwt_decoder_factory(token_type=TokenTypesEnum.access)),
]
LoginAndIssueJWTUseCase = Annotated[
    UserLoginAndIssueJWTUseCaseImpl, Depends(get_auth_and_jwt_use_case)
]
RefreshJWTUseCase = Annotated[RefreshJWTUseCaseImpl, Depends(get_refresh_jwt_use_case)]

## Admin Section
CreateUserUseCase = Annotated[CreateUserUseCaseImpl, Depends(get_create_user_use_case)]
ResetPasswordUseCase = Annotated[ResetUserPasswordByAdminUseCaseImpl, Depends(get_reset_password_by_admin_use_case)]

## Users
ChangePasswordUseCase = Annotated[ChangeUserPasswordUseCaseImpl, Depends(get_change_password_use_case)]

## Regions
ReadRegionUseCase = Annotated[ReadRegionUseCaseImpl, Depends(get_read_region_use_case)]
UpdateRegionUseCase = Annotated[UpdateRegionUseCaseImpl, Depends(get_update_region_use_case)]

## PassportGroups


## TrafficLightObjects
