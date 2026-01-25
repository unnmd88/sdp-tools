from typing import Annotated

from fastapi import Depends
from fastapi.params import Form
from fastapi.security import (
HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
)
from application.interfaces.use_cases.create_user_use_case_interface import (
    CreateUserUseCaseProtocol,
)
from application.use_cases.users.get_user_use_case import GetUserUseCaseImpl
from application.use_cases.users.refresh_jwt_use_case import RefreshJWTUseCaseImpl
from application.use_cases.users.user_login_and_issue_jwt_use_case import UserLoginAndIssueJWTUseCaseImpl

from domain.tlo.services.main_tlo_service import TrafficLightObjectServiceImpl
from domain.users.entities.user import UserEntity
from presentation.api.dependencies.dependencies import (
    users_use_case,
    get_access_jwt_payload_schema,
    is_superuser,
    is_admin,
    get_user_entity_by_id,
    get_refresh_jwt_payload_schema,
    get_auth_and_jwt_use_case,
    get_refresh_jwt_use_case,
    create_user_use_case, oauth2_scheme,
)
from presentation.api.dependencies.utils import get_filters_for_region_or_name_search
from presentation.schemas.auth import AuthSchema
from presentation.schemas.jwt import PayloadAccessJWTSchema, PayloadRefreshJWTSchema


def auth_form(
    username: str = Form(),
    password: str = Form(),
):
    return AuthSchema(username=username, password=password)


## Auth and JWT
BEARER_TOKEN = Annotated[str, Depends(oauth2_scheme)]
AuthForm = Annotated[AuthSchema, Depends(auth_form)]
# AccessAndRefreshJWT = Annotated[TokenInfo, Depends()]
RefreshJWTUseCase = Annotated[RefreshJWTUseCaseImpl, Depends(get_refresh_jwt_use_case)]
LoginAndIssueJWTUseCase = Annotated[
    UserLoginAndIssueJWTUseCaseImpl, Depends(get_auth_and_jwt_use_case)
]
# ManagerJWTDep = Annotated[JWTHelper, Depends(JWTHelper)]
PayloadAccessJWT = Annotated[
    PayloadAccessJWTSchema, Depends(get_access_jwt_payload_schema)
]
PayloadRefreshJWT = Annotated[
    PayloadRefreshJWTSchema, Depends(get_refresh_jwt_payload_schema)
]
IsSuperuser = Depends(is_superuser)
IsAdmin = Depends(is_admin)
# TO DO  AccessFromRefreshJWT = Annotated[TokenInfo, Depends(auth_user_and_issue_access_and_refresh_jwt)]


## Users
UsersUseCase = Annotated[GetUserUseCaseImpl, Depends(users_use_case)]
CreateUserUseCase = Annotated[CreateUserUseCaseProtocol, Depends(create_user_use_case)]
UserEntityDep = Annotated[UserEntity, Depends(get_user_entity_by_id)]

## Regions

regions_filters_for_search = Annotated[
    int | str, Depends(get_filters_for_region_or_name_search)
]
## PassportGroups


## TrafficLightObjects
