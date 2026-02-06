from fastapi.security import (
    HTTPBearer,
    OAuth2PasswordBearer,
)

from application.services.auth_service import AuthenticationService
from application.services.regions_service import RegionsServiceImpl
from application.services.user_service import UserServiceImpl
from application.use_cases.admin.change_password_use_case import ResetUserPasswordByAdminUseCaseImpl
from application.use_cases.admin.create_user_use_case import CreateUserUseCaseImpl
from application.use_cases.regions.read_region_use_case import ReadRegionUseCaseImpl
from application.use_cases.regions.update_regions_use_case import UpdateRegionUseCaseImpl
from application.use_cases.users.change_password_use_case import ChangeUserPasswordUseCaseImpl

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
from domain.repositories.regions_repo_interface import RegionsRepositoryProtocol
from domain.repositories.users_repo_interface import UsersRepositoryProtocol

from infrastructure.auth.jwt.jwt_service import DecodeJWTService, IssueJWTService
from infrastructure.auth.jwt.rules import DecodeJWTSettings, IssueJWTSettings

from infrastructure.auth.password_service import BcryptPasswordService
from infrastructure.database.api import DatabaseAPI
from infrastructure.database.regions_repository import RegionsSqlAlchemyRepository
from infrastructure.database.uow import SQLAlchemyUnitOfWork

from infrastructure.database.user_reposirory import UsersSqlAlchemyRepository


#  -- extras --

http_bearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.login_url)
BEARER_TOKEN = Annotated[str, Depends(oauth2_scheme)]

#  -- sql-alchemy/repo/database --

db_api = DatabaseAPI(
    url=str(settings.db.url),
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)
db_session = Annotated[AsyncSession, Depends(db_api.session_getter)]


def get_users_sqlalchemy_repository(session: db_session) -> UsersSqlAlchemyRepository:
    return UsersSqlAlchemyRepository(session=session)


def get_regions_sqlalchemy_repository(session: db_session) -> RegionsSqlAlchemyRepository:
    return RegionsSqlAlchemyRepository(session=session)

# -- services --


def get_user_service(
    user_repository: Annotated[
        UsersRepositoryProtocol, Depends(get_users_sqlalchemy_repository),
    ]
) -> UserServiceImpl:
    return UserServiceImpl(user_repository=user_repository)


def get_regions_service(
    regions_repository: Annotated[
        RegionsRepositoryProtocol, Depends(get_regions_sqlalchemy_repository),
    ]
) -> RegionsServiceImpl:
    return RegionsServiceImpl(regions_repository=regions_repository)


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

    async def __call__(self, token: BEARER_TOKEN):
        decoded_token = self._method(token)
        if self._specific_field is None:
            return decoded_token
        return getattr(decoded_token, self._specific_field)


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
        user_service=UserServiceImpl(user_repository=user_repository),
        password_service=BcryptPasswordService(),
    )
    return UserLoginAndIssueJWTUseCaseImpl(
        auth_service=auth_service,
        jwt_service=jwt_service,
    )


def get_refresh_jwt_use_case(
    jwt_service: Annotated[IssueJWTServiceDep, Depends(IssueJWTServiceDep())],
    user_repository: Annotated[
        UsersRepositoryProtocol, Depends(get_users_sqlalchemy_repository)
    ],
) -> RefreshJWTUseCaseImpl:
    return RefreshJWTUseCaseImpl(
        jwt_service=jwt_service,
        user_service=UserServiceImpl(user_repository=user_repository),
    )


def get_change_password_use_case(
    user_service: Annotated[UserServiceImpl, Depends(get_user_service)],
    password_service: Annotated[BcryptPasswordService, Depends(BcryptPasswordService)],
) -> ChangeUserPasswordUseCaseImpl:
    return ChangeUserPasswordUseCaseImpl(
        user_service=user_service,
        password_service=password_service
    )

def get_read_region_use_case(
    regions_service: Annotated[RegionsServiceImpl, Depends(get_regions_service)],
) -> ReadRegionUseCaseImpl:
    return ReadRegionUseCaseImpl(regions_service=regions_service)


def get_update_region_use_case(
    session: db_session,
) -> UpdateRegionUseCaseImpl:
    uow = SQLAlchemyUnitOfWork(session=session)
    regions_repository = RegionsSqlAlchemyRepository(session=session)
    user_repository = UsersSqlAlchemyRepository(session=session)
    user_service = UserServiceImpl(user_repository=user_repository)
    regions_service = RegionsServiceImpl(regions_repository=regions_repository)
    return UpdateRegionUseCaseImpl(
        uow=uow,
        regions_service=regions_service,
        user_service=user_service,
    )


# -- ADMIN SECTION  --

def get_create_user_use_case(
    user_service: Annotated[UserServiceImpl, Depends(get_user_service)],
    password_service: Annotated[BcryptPasswordService, Depends(BcryptPasswordService)],
) -> CreateUserUseCaseImpl:
    return CreateUserUseCaseImpl(
        user_service=user_service,
        password_service=password_service
    )


def get_reset_password_by_admin_use_case(
    user_service: Annotated[UserServiceImpl, Depends(get_user_service)],
    password_service: Annotated[BcryptPasswordService, Depends(BcryptPasswordService)],
) -> ResetUserPasswordByAdminUseCaseImpl:
    return ResetUserPasswordByAdminUseCaseImpl(
        user_service=user_service,
        password_service=password_service
    )