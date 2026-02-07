import logging
from collections.abc import AsyncGenerator

from dishka import Provider, Scope, provide
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from app_logging.dev.config import INFRASTRUCTURE
from application.services.auth_service import AuthenticationService
from application.services.regions_service import RegionsServiceImpl
from application.services.user_service import UserServiceImpl
from application.use_cases.admin.change_password_use_case import (
    ResetUserPasswordByAdminUseCaseImpl,
)
from application.use_cases.admin.create_user_use_case import CreateUserUseCaseImpl
from application.use_cases.regions.create_region_use_case import CreateRegionUseCaseImpl
from application.use_cases.regions.delete_region_use_case import DeleteRegionUseCaseImpl
from application.use_cases.regions.read_region_use_case import ReadRegionUseCaseImpl
from application.use_cases.regions.update_regions_use_case import (
    UpdateRegionUseCaseImpl,
)
from application.use_cases.users.change_password_use_case import (
    ChangeUserPasswordUseCaseImpl,
)
from application.use_cases.users.get_active_user_from_repo_use_case import (
    GetActiveUserFromRepoUseCase,
)
from application.use_cases.users.refresh_jwt_use_case import RefreshJWTUseCaseImpl
from application.use_cases.users.user_login_and_issue_jwt_use_case import (
    UserLoginAndIssueJWTUseCaseImpl,
)
from infrastructure.auth.jwt.jwt_service import IssueJWTService, DecodeJWTService
from infrastructure.auth.jwt.rules import IssueJWTSettings, DecodeJWTSettings
from infrastructure.auth.password_service import BcryptPasswordService
from infrastructure.database.api import DatabaseAPI
from infrastructure.database.regions_repository import RegionsSqlAlchemyRepository
from infrastructure.database.uow import SQLAlchemyUnitOfWork
from infrastructure.database.user_reposirory import UsersSqlAlchemyRepository
from core.config import settings as core_settings, Settings


class ConfigProvider(Provider):
    @provide(scope=Scope.APP)
    def get_config(self) -> Settings:
        return core_settings


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    def get_database_api(self, settings: Settings) -> DatabaseAPI:
        return DatabaseAPI(
            url=str(settings.db.url),
            echo=settings.db.echo,
            echo_pool=settings.db.echo_pool,
            pool_size=settings.db.pool_size,
            max_overflow=settings.db.max_overflow,
        )

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, db_api: DatabaseAPI
    ) -> AsyncGenerator[AsyncSession, None]:
        session = db_api.session_factory()
        try:
            yield session
        finally:
            await session.close()

    @provide(scope=Scope.REQUEST)
    def get_unit_of_work(self, session: AsyncSession) -> SQLAlchemyUnitOfWork:
        return SQLAlchemyUnitOfWork(session=session)


class RepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_users_repository(self, session: AsyncSession) -> UsersSqlAlchemyRepository:
        return UsersSqlAlchemyRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def get_regions_repository(
        self, session: AsyncSession
    ) -> RegionsSqlAlchemyRepository:
        return RegionsSqlAlchemyRepository(session=session)


class JWTProvider(Provider):
    """Только создание JWT сервисов, без логики получения токенов"""

    @provide(scope=Scope.APP)
    def get_issue_jwt_settings(self) -> IssueJWTSettings:
        return IssueJWTSettings()

    @provide(scope=Scope.REQUEST)
    def get_issue_jwt_service(self, jwt_settings: IssueJWTSettings) -> IssueJWTService:
        return IssueJWTService(
            private_key=jwt_settings.private_key_path.resolve().read_text("utf-8"),
            algorithm=jwt_settings.algorithm,
            expire_minutes_access_token=jwt_settings.expire_minutes_access_token,
            expire_days_refresh_token=jwt_settings.expire_days_refresh_token,
        )


class ServiceProvider(Provider):
    # User/Auth section
    @provide(scope=Scope.REQUEST)
    def get_user_service(
        self, users_repo: UsersSqlAlchemyRepository
    ) -> UserServiceImpl:
        return UserServiceImpl(user_repository=users_repo)

    @provide(scope=Scope.REQUEST)
    def get_auth_service(self, user_service: UserServiceImpl) -> AuthenticationService:
        return AuthenticationService(
            user_service=user_service,
            password_service=BcryptPasswordService(),
        )

    @provide(scope=Scope.REQUEST)
    def get_password_service(self) -> BcryptPasswordService:
        return BcryptPasswordService()

    # Regions section
    @provide(scope=Scope.REQUEST)
    def get_regions_service(
        self, regions_repo: RegionsSqlAlchemyRepository
    ) -> RegionsServiceImpl:
        return RegionsServiceImpl(regions_repository=regions_repo)


class AdminUseCasesProvider(Provider):
    # +
    @provide(scope=Scope.REQUEST)
    def get_create_user_use_case(
        self,
        uow: SQLAlchemyUnitOfWork,
        user_service: UserServiceImpl,
        password_service: BcryptPasswordService,
    ) -> CreateUserUseCaseImpl:
        return CreateUserUseCaseImpl(
            uow=uow,
            user_service=user_service,
            password_service=password_service,
        )

    # TODO: Проверить, что это работает
    @provide(scope=Scope.REQUEST)
    def get_reset_password_admin_use_case(
        self,
        user_service: UserServiceImpl,
        password_service: BcryptPasswordService,
    ) -> ResetUserPasswordByAdminUseCaseImpl:
        return ResetUserPasswordByAdminUseCaseImpl(
            user_service=user_service, password_service=password_service
        )


class UseCaseProvider(Provider):
    # User/Auth section
    @provide(scope=Scope.REQUEST)
    def get_active_user_use_case(
        self, users_repo: UsersSqlAlchemyRepository
    ) -> GetActiveUserFromRepoUseCase:
        return GetActiveUserFromRepoUseCase(user_repository=users_repo)

    # +
    @provide(scope=Scope.REQUEST)
    def get_login_and_jwt_use_case(
        self,
        auth_service: AuthenticationService,
        jwt_service: IssueJWTService,
    ) -> UserLoginAndIssueJWTUseCaseImpl:
        return UserLoginAndIssueJWTUseCaseImpl(
            auth_service=auth_service,
            jwt_service=jwt_service,
        )

    # +
    @provide(scope=Scope.REQUEST)
    def get_refresh_jwt_use_case(
        self,
        jwt_service: IssueJWTService,
        user_service: UserServiceImpl,
    ) -> RefreshJWTUseCaseImpl:
        return RefreshJWTUseCaseImpl(
            jwt_service=jwt_service,
            user_service=user_service,
        )

    # +
    @provide(scope=Scope.REQUEST)
    def get_change_password_use_case(
        self,
        uow: SQLAlchemyUnitOfWork,
        user_service: UserServiceImpl,
        password_service: BcryptPasswordService,
    ) -> ChangeUserPasswordUseCaseImpl:
        return ChangeUserPasswordUseCaseImpl(
            uow=uow, user_service=user_service, password_service=password_service
        )

    # Regions section
    @provide(scope=Scope.REQUEST)
    def get_read_region_use_case(
        self, regions_service: RegionsServiceImpl
    ) -> ReadRegionUseCaseImpl:
        return ReadRegionUseCaseImpl(regions_service=regions_service)

    @provide(scope=Scope.REQUEST)
    def get_update_region_use_case(
        self,
        uow: SQLAlchemyUnitOfWork,
        user_service: UserServiceImpl,
        regions_service: RegionsServiceImpl,
    ) -> UpdateRegionUseCaseImpl:
        return UpdateRegionUseCaseImpl(
            uow=uow,
            regions_service=regions_service,
            user_service=user_service,
        )

    @provide(scope=Scope.REQUEST)
    def create_region_use_case(
        self,
        uow: SQLAlchemyUnitOfWork,
        user_service: UserServiceImpl,
        regions_service: RegionsServiceImpl,
    ) -> CreateRegionUseCaseImpl:
        return CreateRegionUseCaseImpl(
            uow=uow,
            regions_service=regions_service,
            user_service=user_service,
        )

    @provide(scope=Scope.REQUEST)
    def delete_region_use_case(
        self,
        uow: SQLAlchemyUnitOfWork,
        user_service: UserServiceImpl,
        regions_service: RegionsServiceImpl,
    ) -> DeleteRegionUseCaseImpl:
        return DeleteRegionUseCaseImpl(
            uow=uow,
            regions_service=regions_service,
            user_service=user_service,
        )
