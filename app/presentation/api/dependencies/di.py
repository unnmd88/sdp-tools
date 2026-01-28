from functools import lru_cache

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
)
from jwt import ExpiredSignatureError, DecodeError

from application.services.auth_service import AuthenticationService

from application.use_cases.users.create_user_use_case import CreateUserUseCaseImpl

from application.use_cases.users.refresh_jwt_use_case import RefreshJWTUseCaseImpl
from core.config import settings

from application.use_cases.users.user_login_and_issue_jwt_use_case import (
    UserLoginAndIssueJWTUseCaseImpl,
)
from application.use_cases.users.get_user_use_case import GetUserUseCaseImpl

from typing import Annotated, Literal

from fastapi.params import Depends
from fastapi.exceptions import HTTPException
from starlette import status

from sqlalchemy.ext.asyncio.session import AsyncSession


from domain.enums.unsorted import Roles, TokenTypesEnum
from domain.repositories.users_repo_interface import UsersRepositoryProtocol

from infrastructure.auth.jwt.jwt_service import JWTService
from infrastructure.auth.jwt.rules import JWTSecurityRules, JWTExpireRules, SettingsJWT
from infrastructure.auth.password_service import BcryptPasswordService
from infrastructure.database.api import db_api
from infrastructure.database.passport_groups_repository import (
    PassportGroupsRepositorySqlAlchemyRepository,
)
from infrastructure.database.regions_repository import RegionsRepositorySqlAlchemyRepository
from infrastructure.database.tlo_repository import TrafficLightObjectSqlAlchemyRepository
from infrastructure.database.user_reposirory import UsersSqlAlchemyRepository
from infrastructure.exceptions import RottenTokenError, TokenError

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


def get_users_sqlalchemy_repository(session: db_session) -> UsersSqlAlchemyRepository:
    return UsersSqlAlchemyRepository(session=session)

# -- services --


# -- auth and jwt --


class ExtractPayloadFromJWT:
    def __init__(
        self,
        *,
        token_type: TokenTypesEnum,
        token_settings: SettingsJWT = SettingsJWT(),

    ):
        self.token_settings = token_settings
        self.token_type = token_type
        self.jwt_service = JWTService(
            expire_minutes_access_token=self.token_settings.expire_minutes_access_token,
            expire_days_refresh_token=self.token_settings.expire_days_refresh_token,
            public_key=self.token_settings.public_key_path.resolve().read_text("utf-8"),
            private_key=self.token_settings.private_key_path.resolve().read_text("utf-8"),
            algorithm=self.token_settings.algorithm,
        )

    async def __call__(self,token: Annotated[str, Depends(oauth2_scheme)]):
        try:
            token_dto = self.jwt_service.decode_jwt(token)
        except RottenTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Требуется аутентификация.",
            )
        except TokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Некорректный токен.",
            )
        if token_dto.typ != self.token_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Некорректный тип токена. Ожидаемый тип: {str(self.token_type)}.",
            )
        return token_dto




# -- use-cases --


def users_use_case(
    user_repository: Annotated[
        UsersRepositoryProtocol, Depends(get_users_sqlalchemy_repository)
    ],
) -> GetUserUseCaseImpl:
    return GetUserUseCaseImpl(user_repository=user_repository)


# def create_user_use_case(
#     user_repository: Annotated[
#         UsersRepositoryProtocol, Depends(get_users_sqlalchemy_repository)
#     ],
# ) -> CreateUserUseCaseProtocol:
#     return CreateUserUseCaseImpl(
#         user_repository=user_repository,
#         get_user_use_case=GetUserUseCaseImpl(user_repository=user_repository),
#     )


def get_auth_and_jwt_use_case(
    user_repository: Annotated[
        UsersRepositoryProtocol, Depends(get_users_sqlalchemy_repository)
    ],
) -> UserLoginAndIssueJWTUseCaseImpl:
    auth_service = AuthenticationService(
        user_repository=user_repository,
        password_service=BcryptPasswordService(),
    )
    security_rules = JWTSecurityRules()
    expire_rules = JWTExpireRules()
    jwt_service = JWTService(
        expire_minutes_access_token=expire_rules.expire_minutes_access_token,
        expire_days_refresh_token=expire_rules.expire_days_refresh_token,
        public_key=security_rules.public_key_path,
        private_key=security_rules.private_key_path,
        algorithm=security_rules.algorithm,
    )
    return UserLoginAndIssueJWTUseCaseImpl(
        auth_service=auth_service,
        jwt_service=jwt_service,
    )


def get_refresh_jwt_use_case(
    user_repository: Annotated[
        UsersRepositoryProtocol, Depends(get_users_sqlalchemy_repository)
    ],
) -> RefreshJWTUseCaseImpl:
    return RefreshJWTUseCaseImpl(user_repository=user_repository)
