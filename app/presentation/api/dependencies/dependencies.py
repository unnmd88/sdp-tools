from textwrap import dedent

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import ExpiredSignatureError

from application.interfaces.repositories.passport_groups import PassportGroupRepositoryProtocol
from application.interfaces.repositories.regions import RegionsRepositoryProtocol
from application.interfaces.repositories.tlo import TrafficLightObjectRepositoryProtocol
from application.interfaces.repositories.users import UsersRepositoryProtocol
from application.interfaces.services.authentication import (
    UserAuthenticationServiceProtocol,
)
from application.interfaces.services.passport_groups_crud import PassportGroupsServiceProtocol
from application.interfaces.services.regions_crud import RegionsServiceProtocol
from application.interfaces.services.tlo import TrafficLightObjectServiceProtocol
from application.interfaces.services.users_crud import UsersServiceProtocol
from application.jwt_utils import decode_jwt
from application.use_cases.auth.auth_and_issue_jwt import AuthJWTUseCaseImpl
from application.use_cases.passport_groups.crud import PassportGroupsCrudUseCaseImpl
from application.use_cases.regions.crud import RegionsCrudUseCaseImpl
from application.use_cases.tlo.tlo_use_case import TrafficLightObjectUseCaseImpl
from application.use_cases.users.crud import UsersCrudUseCaseImpl

from typing import Annotated

from fastapi.params import Depends
from fastapi.exceptions  import  HTTPException
from starlette import status

from sqlalchemy.ext.asyncio.session import AsyncSession

from core.dto.users import SearchUserByIdDTO
from core.enums import Roles, TokenTypes
from core.passport_groups.services.crud import PassportGroupsServiceImpl
from core.regions.services.crud import RegionsServiceImpl
from core.security_policies.services.auth import UserAuthenticationServiceImpl
from core.tlo.services.main_tlo_service import TrafficLightObjectServiceImpl
from core.users.entities.user import UserEntity
from core.users.services.crud import UsersServiceImpl
from infrastructure.database.api import db_api
from infrastructure.database.passport_groups_repository import PassportGroupsRepositorySqlAlchemy
from infrastructure.database.regions_repository import RegionsRepositorySqlAlchemy
from infrastructure.database.tlo_repository import TrafficLightObjectSqlAlchemy
from infrastructure.database.user_reposirory import UsersRepositorySqlAlchemy
from presentation.api.exceptions import InvalidErrorJWT

from presentation.schemas.jwt import PayloadAccessJWTSchema, TokenInfo, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE, \
    PayloadRefreshJWTSchema

#  -- extras --

http_bearer = HTTPBearer()


db_session = Annotated[
    AsyncSession,
    Depends(db_api.session_getter),
]

# -- JWT, credentials and access-levels --

def get_jwt_payload_schema(
    credentials: str,
    expected_token_type: TokenTypes,
) -> PayloadAccessJWTSchema | PayloadRefreshJWTSchema:
    try:
        payload = decode_jwt(credentials)
        if payload['typ'] == expected_token_type and expected_token_type == TokenTypes.access:
            return PayloadAccessJWTSchema(**payload)
        elif payload['typ'] == expected_token_type and expected_token_type == TokenTypes.refresh:
            return PayloadRefreshJWTSchema(**payload)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f'Некорректный тип токена. Ожидаемый тип: {str(expected_token_type)}.',
            )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Срок действия токена истёк.',
        )


def get_access_jwt_payload_schema(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
) -> PayloadAccessJWTSchema:
    return get_jwt_payload_schema(
        credentials=credentials.credentials,
        expected_token_type=TokenTypes.access,
    )


def get_refresh_jwt_payload_schema(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
) -> PayloadRefreshJWTSchema:
    return get_jwt_payload_schema(
        credentials=credentials.credentials,
        expected_token_type=TokenTypes.refresh,
    )


def is_admin(
    payload: Annotated[PayloadAccessJWTSchema, Depends(get_access_jwt_payload_schema)]
):
    if not payload.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Доступ запрещен'
        )


def is_superuser(
    payload: Annotated[PayloadAccessJWTSchema, Depends(get_access_jwt_payload_schema)]
):
    if payload.role != Roles.superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Доступ запрещен.'
        )


#  -- sql-alchemy repo --


def get_users_sqlalchemy_repository(session: db_session) -> UsersRepositorySqlAlchemy:
    return UsersRepositorySqlAlchemy(session=session)


def get_regions_sqlalchemy_repository(session: db_session) -> RegionsRepositoryProtocol:
    return RegionsRepositorySqlAlchemy(session=session)


def get_passport_groups_sqlalchemy_repository(session: db_session) -> RegionsRepositoryProtocol:
    return PassportGroupsRepositorySqlAlchemy(session=session)


def get_tlo_sqlalchemy_repository(session: db_session) -> TrafficLightObjectRepositoryProtocol:
    return TrafficLightObjectSqlAlchemy(session=session)

#  -- cache --


# -- services --


def get_crud_users_service(
    sqlalchemy_repository: Annotated[
        UsersRepositoryProtocol, Depends(get_users_sqlalchemy_repository)
    ],
) -> UsersServiceProtocol:
    return UsersServiceImpl(
        repository=sqlalchemy_repository,
    )


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


async def get_user_entity_by_id(
    payload_jwt: Annotated[PayloadAccessJWTSchema, Depends(get_access_jwt_payload_schema)],
    users_crud: Annotated[UsersCrudUseCaseImpl, Depends(users_crud_use_case)]
):
    dto = SearchUserByIdDTO(customer_id=payload_jwt.user_id, search_user_id=payload_jwt.user_id)
    if (user_entity := await users_crud.get_user_by_id(dto)) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Пользователь с id={payload_jwt.user_id!r} не найден.'
        )
    return user_entity


def get_regions_service(
    user: Annotated[UserEntity, Depends(get_user_entity_by_id)],
    sqlalchemy_repository: Annotated[
        RegionsRepositoryProtocol, Depends(get_regions_sqlalchemy_repository)
    ],
) -> RegionsServiceProtocol:
    return RegionsServiceImpl(
        user_entity=user,
        repository=sqlalchemy_repository
    )


def get_regions_crud_use_case(
    region_service: Annotated[RegionsServiceProtocol, Depends(get_regions_service)]
):
    return RegionsCrudUseCaseImpl(regions_service=region_service)


def get_passport_groups_service(
    user: Annotated[UserEntity, Depends(get_user_entity_by_id)],
    sqlalchemy_repository: Annotated[
        PassportGroupRepositoryProtocol, Depends(get_passport_groups_sqlalchemy_repository)
    ],
) -> PassportGroupsServiceProtocol:
    return PassportGroupsServiceImpl(
        user_entity=user,
        repository=sqlalchemy_repository
    )


def get_passport_groups_use_case(
    passport_group_service: Annotated[PassportGroupsServiceImpl, Depends(get_passport_groups_service)]
):
    return PassportGroupsCrudUseCaseImpl(passport_group_service=passport_group_service)


def get_tlo_service(
    user: Annotated[UserEntity, Depends(get_user_entity_by_id)],
    sqlalchemy_repository: Annotated[
        TrafficLightObjectRepositoryProtocol, Depends(get_tlo_sqlalchemy_repository)
    ],
) -> TrafficLightObjectServiceProtocol:
    return TrafficLightObjectServiceImpl(
        user_entity=user,
        repository=sqlalchemy_repository,
    )


def get_tlo_use_case(
    tlo_service: Annotated[TrafficLightObjectServiceImpl, Depends(get_tlo_service)]
):
    return TrafficLightObjectUseCaseImpl(tlo_service=tlo_service)