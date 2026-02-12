from collections.abc import AsyncGenerator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from application.base_crud_use_cases import (
    BaseReadUseCase,
    BaseCreateUseCase,
    BaseUpdateUseCase,
    BaseDeleteUseCase,
)
from application.dto.passport_groups_dto import PassportGroupDTO
from application.dto.regions_dto import RegionDTO
from application.dto.tlo_dto import TrafficLightObjectDTO
from application.services.auth_service import AuthenticationService
from application.services.passport_group_service import PassportGroupServiceImpl
from application.services.regions_service import RegionsServiceImpl
from application.services.tlo_service import TrafficLightObjectServiceImpl
from application.services.user_service import UserServiceImpl
from application.use_cases.admin.change_password_use_case import (
    ResetUserPasswordByAdminUseCaseImpl,
)
from application.use_cases.admin.create_user_use_case import CreateUserUseCaseImpl
from application.use_cases.passport_groups.passport_group_read_use_case import (
    PassportGroupReadByNameUseCase,
)
from application.use_cases.passport_groups.types import (
    PassportGroupReadUseCase,
    PassportGroupCreateUseCase,
    PassportGroupUpdateUseCase,
    PassportGroupDeleteUseCase,
)

from application.use_cases.regions.region_read_use_case import (
    RegionReadByCodeOrNameUseCase,
)
from application.use_cases.regions.types import (
    RegionReadUseCase,
    RegionCreateUseCase,
    RegionUpdateUseCase,
)
from application.use_cases.tlo_use_cases.types import TrafficLightObjectsReadUseCase, TrafficLightObjectsCreateUseCase

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
from infrastructure.auth.jwt.jwt_service import IssueJWTService
from infrastructure.auth.jwt.rules import IssueJWTSettings
from infrastructure.auth.password_service import BcryptPasswordService
from infrastructure.database.api import DatabaseAPI
from infrastructure.database.base_adapter_wrapper import BaseRepositoryAdapterWrapper
from infrastructure.database.mappers.tlo_mapper import TrafficLightObjectDBMapper
from infrastructure.database.models import TrafficLightObject as TrafficLightObjectModel
from infrastructure.database.passport_groups_repository import (
    PassportGroupsSqlAlchemyRepository,
)
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

    @provide(scope=Scope.REQUEST)
    def passport_groups_repository(
        self, session: AsyncSession
    ) -> PassportGroupsSqlAlchemyRepository:
        return PassportGroupsSqlAlchemyRepository(session=session)

    # @provide(scope=Scope.REQUEST)
    # def traffic_light_objects_repository(self, session: AsyncSession) -> BaseRepositoryAdapterWrapper:
    #     return BaseRepositoryAdapterWrapper(
    #         session=session,
    #         model=TrafficLightObjectModel,
    #         mapper=TrafficLightObjectDBMapper(),
    #     )


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


class ServicesProvider(Provider):
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
        return RegionsServiceImpl(repository=regions_repo)

    # Passport-groups section
    @provide(scope=Scope.REQUEST)
    def passport_groups_service(
        self, passport_groups_repo: PassportGroupsSqlAlchemyRepository
    ) -> PassportGroupServiceImpl:
        return PassportGroupServiceImpl(repository=passport_groups_repo)


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


class TrafficLightObjectsUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def base_read_traffic_light_object_use_case(
        self, session: AsyncSession
    ) -> TrafficLightObjectsReadUseCase:
        repo_wrapper = BaseRepositoryAdapterWrapper(
            session=session,
            model=TrafficLightObjectModel,
            mapper=TrafficLightObjectDBMapper(),
        )
        return BaseReadUseCase(
            entity_service=TrafficLightObjectServiceImpl(repository=repo_wrapper),
            to_dto_mapper=TrafficLightObjectDTO,
        )

    @provide(scope=Scope.REQUEST)
    def base_create_traffic_light_object_use_case(
        self,
        user_service: UserServiceImpl,
        uow: SQLAlchemyUnitOfWork,

    ) -> TrafficLightObjectsCreateUseCase:
        repo_wrapper = BaseRepositoryAdapterWrapper(
            session=uow.session,
            model=TrafficLightObjectModel,
            mapper=TrafficLightObjectDBMapper(),
        )
        return BaseCreateUseCase(
            uow=uow,
            user_service=user_service,
            entity_service=TrafficLightObjectServiceImpl(repository=repo_wrapper),
            to_dto_mapper=TrafficLightObjectDTO,
        )


class PassportGroupUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def base_read_passport_groups_use_case(
        self, passport_groups_service: PassportGroupServiceImpl
    ) -> PassportGroupReadUseCase:
        return BaseReadUseCase(
            entity_service=passport_groups_service,
            to_dto_mapper=PassportGroupDTO,
        )

    @provide(scope=Scope.REQUEST)
    def read_passport_groups_by_name_use_case(
        self, passport_groups_service: PassportGroupServiceImpl
    ) -> PassportGroupReadByNameUseCase:
        return PassportGroupReadByNameUseCase(pg_service=passport_groups_service)

    @provide(scope=Scope.REQUEST)
    def create_passport_group_use_case(
        self,
        uow: SQLAlchemyUnitOfWork,
        user_service: UserServiceImpl,
        passport_groups_service: PassportGroupServiceImpl,
    ) -> PassportGroupCreateUseCase:
        """Use case для создания PassportGroup"""
        return BaseCreateUseCase(
            uow=uow,
            user_service=user_service,
            entity_service=passport_groups_service,
            to_dto_mapper=PassportGroupDTO,
        )

    @provide(scope=Scope.REQUEST)
    def update_passport_group_use_case(
        self,
        uow: SQLAlchemyUnitOfWork,
        user_service: UserServiceImpl,
        passport_groups_service: PassportGroupServiceImpl,
    ) -> PassportGroupUpdateUseCase:
        return BaseUpdateUseCase(
            uow=uow,
            entity_service=passport_groups_service,
            user_service=user_service,
            to_dto_mapper=PassportGroupDTO,
        )

    @provide(scope=Scope.REQUEST)
    def delete_passport_group_use_case(
        self,
        uow: SQLAlchemyUnitOfWork,
        user_service: UserServiceImpl,
        passport_groups_service: PassportGroupServiceImpl,
    ) -> PassportGroupDeleteUseCase:
        return BaseDeleteUseCase(
            uow=uow,
            entity_service=passport_groups_service,
            user_service=user_service,
            to_dto_mapper=PassportGroupDTO,
        )


class RegionsUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def base_read_regions_use_case(
        self, regions_service: RegionsServiceImpl
    ) -> RegionReadUseCase:
        return BaseReadUseCase(
            entity_service=regions_service,
            to_dto_mapper=RegionDTO,
        )

    @provide(scope=Scope.REQUEST)
    def read_passport_groups_by_code_or_name_use_case(
        self,
        regions_service: RegionsServiceImpl,
    ) -> RegionReadByCodeOrNameUseCase:
        return RegionReadByCodeOrNameUseCase(regions_service=regions_service)

    @provide(scope=Scope.REQUEST)
    def create_passport_group_use_case(
        self,
        uow: SQLAlchemyUnitOfWork,
        user_service: UserServiceImpl,
        regions_service: RegionsServiceImpl,
    ) -> RegionCreateUseCase:
        """Use case для создания PassportGroup"""
        return BaseCreateUseCase(
            uow=uow,
            user_service=user_service,
            entity_service=regions_service,
            to_dto_mapper=RegionDTO,
        )

    @provide(scope=Scope.REQUEST)
    def update_passport_group_use_case(
        self,
        uow: SQLAlchemyUnitOfWork,
        user_service: UserServiceImpl,
        regions_service: RegionsServiceImpl,
    ) -> RegionUpdateUseCase:
        return BaseUpdateUseCase(
            uow=uow,
            user_service=user_service,
            entity_service=regions_service,
            to_dto_mapper=RegionDTO,
        )

    @provide(scope=Scope.REQUEST)
    def delete_passport_group_use_case(
        self,
        uow: SQLAlchemyUnitOfWork,
        user_service: UserServiceImpl,
        regions_service: RegionsServiceImpl,
    ) -> PassportGroupDeleteUseCase:
        return BaseDeleteUseCase(
            uow=uow,
            user_service=user_service,
            entity_service=regions_service,
            to_dto_mapper=RegionDTO,
        )


class UsersUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_active_user_use_case(
        self, users_repo: UsersSqlAlchemyRepository
    ) -> GetActiveUserFromRepoUseCase:
        return GetActiveUserFromRepoUseCase(user_repository=users_repo)

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
