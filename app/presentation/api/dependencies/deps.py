from typing import Annotated

from fastapi import Depends
from fastapi.params import Form

from application.use_cases.auth.auth_and_issue_jwt import AuthJWTUseCaseImpl
from application.use_cases.regions.crud import RegionsCrudUseCaseImpl
from application.use_cases.users.crud import UsersCrudUseCaseImpl
from core.users.entities.user import UserEntity
from presentation.api.dependencies.dependencies import (
    auth_use_case,
    users_crud_use_case,
    get_jwt_payload_jwt_bearer, get_regions_crud_use_case, is_superuser, is_admin, get_user_entity_by_id,
)
from presentation.schemas.auth import AuthSchema
from presentation.schemas.jwt import PayloadJWTSchema, TokenInfo


def auth_form(
    username: str = Form(),
    password: str = Form(),
):
    return AuthSchema(username=username, password=password)

## Auth
AuthForm = Annotated[AuthSchema, Depends(auth_form)]
JWTAuthUseCase = Annotated[AuthJWTUseCaseImpl, Depends(auth_use_case)]
AccessAndRefreshJWT = Annotated[TokenInfo, Depends()]
PayloadJWTDependency = Annotated[PayloadJWTSchema, Depends(get_jwt_payload_jwt_bearer)]
PayloadJWT = Annotated[PayloadJWTSchema, Depends(get_jwt_payload_jwt_bearer)]
IsSuperuser = Depends(is_superuser)
IsAdmin = Depends(is_admin)
# TO DO  AccessFromRefreshJWT = Annotated[TokenInfo, Depends(auth_user_and_issue_access_and_refresh_jwt)]


## Users
UsersCrudUseCase = Annotated[UsersCrudUseCaseImpl, Depends(users_crud_use_case)]
UserEntityDep = Annotated[UserEntity, Depends(get_user_entity_by_id)]

## Regions
RegionsCrudUseCase = Annotated[RegionsCrudUseCaseImpl, Depends(get_regions_crud_use_case)]


