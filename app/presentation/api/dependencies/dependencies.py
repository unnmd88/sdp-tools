from fastapi import Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from application.interfaces.repositories.users import UsersRepositoryProtocol
from application.interfaces.services.authentication import (
    UserAuthenticationServiceProtocol,
)
from application.interfaces.services.users_crud import UsersServiceProtocol
from application.use_cases.auth.auth_and_issue_jwt import AuthJWTUseCaseImpl
from application.use_cases.users.crud import UsersCrudUseCaseImpl

from typing import Annotated

from fastapi.params import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from auth.utils import decode_jwt
from core.security_policies.services.auth import UserAuthenticationServiceImpl
from core.users.services.crud import UsersServiceImpl
from infrastructure.database.api import db_api
from infrastructure.database.user_reposirory import UsersRepositorySqlAlchemy

from presentation.schemas.jwt import PayloadJWTSchema, TokenInfo


#  -- extras --

http_bearer = HTTPBearer()


db_session = Annotated[
    AsyncSession,
    Depends(db_api.session_getter),
]


def get_jwt_payload_jwt_bearer(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
) -> PayloadJWTSchema:
    print(credentials)
    print(PayloadJWTSchema(**decode_jwt(credentials.credentials)))
    return PayloadJWTSchema(**decode_jwt(credentials.credentials))


#  -- sql-alchemy repo --


def get_sqlalchemy_repository(session: db_session) -> UsersRepositorySqlAlchemy:
    return UsersRepositorySqlAlchemy(session=session)


#  -- cache --


# -- services --


def get_crud_users_service(
    sqlalchemy_repository: Annotated[
        UsersRepositoryProtocol, Depends(get_sqlalchemy_repository)
    ],
) -> UsersServiceProtocol:
    return UsersServiceImpl(repository=sqlalchemy_repository)


def get_auth_service(
    user_service: Annotated[UsersServiceProtocol, Depends(get_crud_users_service)],
):
    return UserAuthenticationServiceImpl(user_service=user_service)


# -- use-cases --


def auth_use_case(
    auth_service: Annotated[
        UserAuthenticationServiceProtocol, Depends(get_auth_service)
    ],
) -> AuthJWTUseCaseImpl:
    return AuthJWTUseCaseImpl(auth_service=auth_service)


def users_crud_use_case(
    service: Annotated[UsersServiceProtocol, Depends(get_crud_users_service)],
) -> UsersCrudUseCaseImpl:
    return UsersCrudUseCaseImpl(user_service=service)


async def get_user_from_jwt(
    payload: Annotated[PayloadJWTSchema, Depends(get_jwt_payload_jwt_bearer)],
) -> UsersServiceImpl:
    pass


AccessAndRefreshJWT = Annotated[TokenInfo, Depends()]
# TO DO  AccessFromRefreshJWT = Annotated[TokenInfo, Depends(auth_user_and_issue_access_and_refresh_jwt)]
PayloadJWTDependency = Annotated[PayloadJWTSchema, Depends(get_jwt_payload_jwt_bearer)]
