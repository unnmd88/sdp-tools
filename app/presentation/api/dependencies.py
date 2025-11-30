from fastapi import Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from application.interfaces.services.authentication import (
    AuthenticationUserServiceProtocol,
)
from application.use_cases.auth.auth import AuthUseCaseImpl
from auth.exceptions import InvalidUsernameOrPasswordException, InactiveUserException
from auth.schemas import AuthSchema, TokenInfo, PayloadJWTSchema

from typing import Annotated

from fastapi.params import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession


from application.use_cases.crud import UsersCrudUseCase
from application.use_cases.users.get_users_from_repo import UsersRepositoryUseCaseImpl
from auth.services.authentication import AuthenticationUserServiceImpl
from auth.utils import decode_jwt
from core.users.services.get_user import UserServiceImpl
from infrastructure.database.api import db_api
from infrastructure.database.tlo_repository import TrafficLightObjectSqlAlchemy
from infrastructure.database.user_reposirory import UsersRepositorySqlAlchemy
from presentation.api.exceptions import (
    InactiveUserErrorHttp403,
    UnauthorizedErrorHttp401,
)

http_bearer = HTTPBearer()


db_session = Annotated[
    AsyncSession,
    Depends(db_api.session_getter),
]


def get_jwt_payload_jwt_bearer(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
):
    return PayloadJWTSchema(**decode_jwt(credentials.credentials))


# use-cases


def get_tlo() -> UsersCrudUseCase:
    return UsersCrudUseCase(repository=TrafficLightObjectSqlAlchemy(session=db_session))


def users_crud() -> UsersRepositoryUseCaseImpl:
    return UsersRepositoryUseCaseImpl(UserServiceImpl())


def auth_form(
    username: str = Form(),
    password: str = Form(),
):
    print('1111111111111111111111111')
    return AuthSchema(username=username, password_plain=password)


def get_auth_user_service(
    user_schema: Annotated[AuthSchema, Depends(auth_form)],
) -> AuthenticationUserServiceProtocol:
    print('2222222222222222222222222')
    print(f'user_schema: {user_schema}')
    return AuthenticationUserServiceImpl(
        UsersRepositorySqlAlchemy,
        user_schema,
    )


def get_auth_user_use_case(
    user_service: Annotated[
        AuthenticationUserServiceProtocol, Depends(get_auth_user_service)
    ],
) -> AuthenticationUserServiceProtocol:
    print('333333333333333333333333333')
    return AuthUseCaseImpl(user_service)


async def auth_user_and_issue_access_and_refresh_jwt(
    user_service: Annotated[
        AuthenticationUserServiceProtocol, Depends(get_auth_user_service)
    ],
) -> TokenInfo:
    try:
        use_case = AuthUseCaseImpl(user_service)
        return await use_case.auth_and_issue_jwt(refresh=True)
    except InvalidUsernameOrPasswordException:
        raise UnauthorizedErrorHttp401
    except InactiveUserException:
        raise InactiveUserErrorHttp403

    # return AuthUseCaseImpl(user_service)


async def get_user_from_jwt() -> UserServiceImpl:
    pass


CrudTloUseCase = Annotated[UsersCrudUseCase, Depends(get_tlo)]
UsersCrudUseCase = Annotated[UsersRepositoryUseCaseImpl, Depends(users_crud)]
AuthUseCase = Annotated[
    AuthenticationUserServiceProtocol, Depends(get_auth_user_use_case)
]
AccessAndRefreshJWT = Annotated[
    TokenInfo, Depends(auth_user_and_issue_access_and_refresh_jwt)
]
# TO DO  AccessFromRefreshJWT = Annotated[TokenInfo, Depends(auth_user_and_issue_access_and_refresh_jwt)]
PayloadJWTDependency = Annotated[PayloadJWTSchema, Depends(get_jwt_payload_jwt_bearer)]
