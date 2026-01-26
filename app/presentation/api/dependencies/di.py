from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
)
from jwt import ExpiredSignatureError, DecodeError

from application.interfaces.repositories.regions import RegionsRepositoryProtocol
from application.interfaces.repositories.tlo import TrafficLightObjectRepositoryProtocol
from application.interfaces.repositories.users_repo_interface import (
    UsersRepositoryProtocol,
)

from application.interfaces.use_cases.create_user_use_case_interface import (
    CreateUserUseCaseProtocol,
)
from application.interfaces.use_cases.get_user_from_repo_by_jwt_use_case_interface import (
    GetUserFromRepoByJWTUseCaseProtocol,
)
from application.interfaces.use_cases.user_login_and_issue_jwt_use_case_interface import (
    UserLoginAndIssueJWTUseCaseProtocol,
)
from application.services.get_user_from_repo_by_jwt_service import (
    GetUserFromRepoByJWTService,
)
from application.use_cases.users.create_user_use_case import CreateUserUseCaseImpl
from application.use_cases.users.get_user_from_repo_by_jwt_use_case import (
    GetUserFromRepoByJWTUseCaseImpl,
)
from application.use_cases.users.refresh_jwt_use_case import RefreshJWTUseCaseImpl
from core.config import settings

from application.use_cases.users.user_login_and_issue_jwt_use_case import (
    UserLoginAndIssueJWTUseCaseImpl,
)
from application.use_cases.users.get_user_use_case import GetUserUseCaseImpl

from typing import Annotated

from fastapi import Request
from fastapi.params import Depends
from fastapi.exceptions import HTTPException
from starlette import status

from sqlalchemy.ext.asyncio.session import AsyncSession

from domain.dto.users import GetUserFromRepoDTO, UserDTO
from domain.enums.unsorted import Roles, TokenTypesEnum
from domain._exceptions.entity_not_found_exc import DomainEntityNotFoundError
from domain._exceptions.permissions_exc import DomainInactiveUserError
from infrastructure.auth.jwt.decode_jwt_service import DecodeJWTService
from infrastructure.auth.jwt.jwt_service import BaseJWTService
from infrastructure.database.api import db_api
from infrastructure.database.passport_groups_repository import (
    PassportGroupsRepositorySqlAlchemy,
)
from infrastructure.database.regions_repository import RegionsRepositorySqlAlchemy
from infrastructure.database.tlo_repository import TrafficLightObjectSqlAlchemy
from infrastructure.database.user_reposirory import UsersRepositorySqlAlchemy


from presentation.schemas.jwt import PayloadAccessJWTSchema, PayloadRefreshJWTSchema

#  -- extras --

http_bearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.login_url)
db_session = Annotated[AsyncSession, Depends(db_api.session_getter)]


# -- JWT, credentials and access-levels --


def get_jwt_payload_schema(
    # credentials: str,
    token: Annotated[str, Depends(oauth2_scheme)],
    expected_token_type: TokenTypesEnum,
) -> PayloadAccessJWTSchema | PayloadRefreshJWTSchema:
    try:
        print(f"TOKEN: {token}")
        # payload = jwt_helper.decode_jwt(credentials)
        payload = jwt_helper.decode_jwt(token)
        if (
            payload["typ"] == expected_token_type
            and expected_token_type == TokenTypesEnum.access
        ):
            return PayloadAccessJWTSchema(**payload)
        elif (
            payload["typ"] == expected_token_type
            and expected_token_type == TokenTypesEnum.refresh
        ):
            return PayloadRefreshJWTSchema(**payload)
        else:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=f"Некорректный тип токена. Ожидаемый тип: {str(expected_token_type)}.",
            )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Срок действия токена истёк.",
        )
    except DecodeError:
        # TODO Залоггировать!
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def get_access_jwt_payload_schema(
    # credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> PayloadAccessJWTSchema:
    return get_jwt_payload_schema(
        # credentials=credentials.credentials,
        token=token,
        expected_token_type=TokenTypesEnum.access,
    )


def get_refresh_jwt_payload_schema(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
) -> PayloadRefreshJWTSchema:
    return get_jwt_payload_schema(
        credentials=credentials.credentials,
        expected_token_type=TokenTypesEnum.refresh,
    )


def is_admin(
    payload: Annotated[PayloadAccessJWTSchema, Depends(get_access_jwt_payload_schema)],
):
    if not payload.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Доступ запрещен"
        )


def is_superuser(
    payload: Annotated[PayloadAccessJWTSchema, Depends(get_access_jwt_payload_schema)],
):
    if payload.role != Roles.superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Доступ запрещен."
        )


#  -- sql-alchemy repo --


def get_users_sqlalchemy_repository(session: db_session) -> UsersRepositorySqlAlchemy:
    return UsersRepositorySqlAlchemy(session=session)


def get_regions_sqlalchemy_repository(session: db_session) -> RegionsRepositoryProtocol:
    return RegionsRepositorySqlAlchemy(session=session)


def get_passport_groups_sqlalchemy_repository(
    session: db_session,
) -> RegionsRepositoryProtocol:
    return PassportGroupsRepositorySqlAlchemy(session=session)


def get_tlo_sqlalchemy_repository(
    session: db_session,
) -> TrafficLightObjectRepositoryProtocol:
    return TrafficLightObjectSqlAlchemy(session=session)


#  -- cache --


# -- services --


# -- use-cases --


class GetUserFromRepoByJWTDep:
    def __init__(
        self,
        *,
        jwt_service: BaseJWTService = BaseJWTService(),
        require_active: bool = True,
        require_role: Roles | None = None,
    ):
        self.jwt_service = jwt_service
        self.require_active = require_active
        self.require_role = require_role

    def __call__(
        self,
        user_repository: Annotated[
            UsersRepositoryProtocol, Depends(get_users_sqlalchemy_repository)
        ],
    ) -> GetUserFromRepoByJWTUseCaseProtocol:
        return GetUserFromRepoByJWTUseCaseImpl(
            service=GetUserFromRepoByJWTService(
                user_repository=user_repository,
                jwt_service=self.jwt_service,
                require_active=self.require_active,
                require_role=self.require_role,
            )
        )


def users_use_case(
    user_repository: Annotated[
        UsersRepositoryProtocol, Depends(get_users_sqlalchemy_repository)
    ],
) -> GetUserUseCaseImpl:
    return GetUserUseCaseImpl(user_repository=user_repository)


def create_user_use_case(
    user_repository: Annotated[
        UsersRepositoryProtocol, Depends(get_users_sqlalchemy_repository)
    ],
) -> CreateUserUseCaseProtocol:
    return CreateUserUseCaseImpl(
        user_repository=user_repository,
        get_user_use_case=GetUserUseCaseImpl(user_repository=user_repository),
    )


def get_auth_and_jwt_use_case(
    user_repository: Annotated[
        UsersRepositoryProtocol, Depends(get_users_sqlalchemy_repository)
    ],
) -> UserLoginAndIssueJWTUseCaseProtocol:
    return UserLoginAndIssueJWTUseCaseImpl(
        user_repository=user_repository,
    )


def get_refresh_jwt_use_case(
    user_repository: Annotated[
        UsersRepositoryProtocol, Depends(get_users_sqlalchemy_repository)
    ],
) -> RefreshJWTUseCaseImpl:
    return RefreshJWTUseCaseImpl(user_repository=user_repository)
