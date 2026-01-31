from functools import lru_cache
from pathlib import Path

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
)
from jwt import ExpiredSignatureError, DecodeError

from application.dto.jwt_dto import AccessJWTPayloadDTO, RefreshJWTPayloadDTO
from application.services.auth_service import AuthenticationService

from application.use_cases.users.create_user_use_case import CreateUserUseCaseImpl
from application.use_cases.users.get_active_user_from_repo_use_case import (
    GetActiveUserFromRepoUseCase,
)

from application.use_cases.users.refresh_jwt_use_case import RefreshJWTUseCaseImpl
from core.config import settings

from application.use_cases.users.user_login_and_issue_jwt_use_case import (
    UserLoginAndIssueJWTUseCaseImpl,
)

from typing import Annotated, Literal

from fastapi.params import Depends
from fastapi.exceptions import HTTPException
from starlette import status

from sqlalchemy.ext.asyncio.session import AsyncSession


from domain.enums.unsorted import Roles, TokenTypesEnum
from domain.repositories.users_repo_interface import UsersRepositoryProtocol

from infrastructure.auth.jwt.jwt_service import DecodeJWTService, IssueJWTService
from infrastructure.auth.jwt.rules import DecodeJWTSettings, IssueJWTSettings

from infrastructure.auth.password_service import BcryptPasswordService
from infrastructure.database.api import db_api
from infrastructure.database.passport_groups_repository import (
    PassportGroupsRepositorySqlAlchemyRepository,
)
from infrastructure.database.regions_repository import (
    RegionsRepositorySqlAlchemyRepository,
)
from infrastructure.database.tlo_repository import (
    TrafficLightObjectSqlAlchemyRepository,
)
from infrastructure.database.user_reposirory import UsersSqlAlchemyRepository
from infrastructure.exceptions import (
    RottenTokenError,
    TokenError,
    InvalidTokenTypeError,
)

from presentation.schemas.jwt import PayloadAccessJWTSchema, PayloadRefreshJWTSchema

#  -- extras --

http_bearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.login_url)
db_session = Annotated[AsyncSession, Depends(db_api.session_getter)]


#  -- sql-alchemy repo --


def get_users_sqlalchemy_repository(session: db_session) -> UsersSqlAlchemyRepository:
    return UsersSqlAlchemyRepository(session=session)


# -- services --


# -- JWT, credentials and access-levels --


class JWTDecoder:
    def __init__(
        self,
        *,
        jwt_service: DecodeJWTService,
        token_type: TokenTypesEnum,
        specific_field: Literal["user_id", "username"] = None,
    ):
        if specific_field == "username":
            self._specific_field = "sub"
        else:
            self._specific_field = specific_field
        self._jwt_service = jwt_service
        self._token_type = token_type
        if self._token_type == TokenTypesEnum.access:
            self._method = self._jwt_service.decode_access_jwt
        elif token_type == TokenTypesEnum.refresh:
            self._method = self._jwt_service.decode_refresh_jwt
        else:
            raise ValueError("Некорректный тип токена.")

    async def __call__(self, token: Annotated[str, Depends(oauth2_scheme)]):
        try:
            decoded_token = self._method(token)
            if self._specific_field is None:
                return decoded_token
            return getattr(decoded_token, self._specific_field)
        except RottenTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Требуется аутентификация.",
            )
        except InvalidTokenTypeError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Некорректный тип токена. Ожидаемый тип: {self._token_type}.",
            )
        except TokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Некорректный токен",
            )


def jwt_decoder_factory(
    *,
    token_type: TokenTypesEnum,
    decode_jwt_settings: DecodeJWTSettings = DecodeJWTSettings(),
    specific_field: Literal["user_id", "username"] = None,
):
    jwt_service = DecodeJWTService(
        public_key=decode_jwt_settings.public_key_path.resolve().read_text("utf-8"),
        algorithm=decode_jwt_settings.algorithm,
    )
    return JWTDecoder(
        jwt_service=jwt_service, token_type=token_type, specific_field=specific_field
    )


class IssueJWTServiceDep:
    def __init__(self, decode_jwt_settings: IssueJWTSettings = IssueJWTSettings()):
        self._decode_jwt_settings = decode_jwt_settings
        self._jwt_service = IssueJWTService(
            private_key=self._decode_jwt_settings.private_key_path.resolve().read_text(
                "utf-8"
            ),
            algorithm=self._decode_jwt_settings.algorithm,
            expire_minutes_access_token=self._decode_jwt_settings.expire_minutes_access_token,
            expire_days_refresh_token=self._decode_jwt_settings.expire_days_refresh_token,
        )

    async def __call__(self) -> IssueJWTService:
        return self._jwt_service


# -- use-cases --


# def users_use_case(
#     user_repository: Annotated[
#         UsersRepositoryProtocol, Depends(get_users_sqlalchemy_repository)
#     ],
# ) -> GetUserUseCaseImpl:
#     return GetUserUseCaseImpl(user_repository=user_repository)


# def create_user_use_case(
#     user_repository: Annotated[
#         UsersRepositoryProtocol, Depends(get_users_sqlalchemy_repository)
#     ],
# ) -> CreateUserUseCaseProtocol:
#     return CreateUserUseCaseImpl(
#         user_repository=user_repository,
#         get_user_use_case=GetUserUseCaseImpl(user_repository=user_repository),
#     )


def get_active_user_use_case(
    repository: Annotated[
        UsersRepositoryProtocol, Depends(get_users_sqlalchemy_repository)
    ],
) -> GetActiveUserFromRepoUseCase:
    return GetActiveUserFromRepoUseCase(user_repository=repository)


def get_auth_and_jwt_use_case(
    jwt_service: Annotated[IssueJWTServiceDep, Depends(IssueJWTServiceDep())],
    user_repository: Annotated[
        UsersRepositoryProtocol, Depends(get_users_sqlalchemy_repository)
    ],
) -> UserLoginAndIssueJWTUseCaseImpl:
    auth_service = AuthenticationService(
        user_repository=user_repository,
        password_service=BcryptPasswordService(),
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
