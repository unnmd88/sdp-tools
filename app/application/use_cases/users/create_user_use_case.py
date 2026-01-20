import logging

from dataclasses import dataclass

from app_logging.dev.config import USERS_LOGGER
from application.interfaces.repositories.users_repo_interface import (
    UsersRepositoryProtocol,
)
from application.interfaces.use_cases.get_user_use_case_interface import (
    GetUserUseCaseProtocol,
)
from application.interfaces.services.entity_factories.base_entity_factory_interface import (
    EntityFactoryServiceProtocol,
)
from application.interfaces.services.user_password_service_interface import (
    UserPasswordServiceProtocol,
)

from domain.dto.users import CreateUserDTO
from domain.enums.unsorted import Organizations, Roles
from domain.exceptions.base import ApplicationError
from domain.exceptions.users import UserPermissionsError
from domain.services.entity_factories.user_entity_factory_service import (
    UserEntityFactoryService,
)
from domain.users.entities.user import UserEntity

# from domain.users.exceptions import (
#     UserNotFoundError,
#     InactiveUserError,
#     UserAlreadyExistsError,
#     InvalidValueToSetError,
# )
from domain.services.user_password_service import hash_password, UserPasswordService
from domain.services.field_values_constraints import UserEntityBusinessRules


logger = logging.getLogger(USERS_LOGGER)


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateUserUseCaseImpl:
    """Класс для создания нового пользователя системы."""

    user_repository: UsersRepositoryProtocol
    get_user_use_case: GetUserUseCaseProtocol
    user_factory: type[EntityFactoryServiceProtocol] = UserEntityFactoryService
    user_password_service: type[UserPasswordServiceProtocol] = UserPasswordService

    async def __call__(self, create_user_dto: CreateUserDTO) -> UserEntity:
        logger.info(
            "Запрос на создание нового пользователя от инициатора=%r: %r",
            create_user_dto.customer,
            create_user_dto,
        )
        try:
            customer_entity: UserEntity = (
                await self.get_user_use_case.get_active_user_or_raise(
                    create_user_dto.customer
                )
            )
            logger.info("Инициатор=%r найден", customer_entity.username)
        except UserNotFoundError:
            msg = f"Ошибка: {create_user_dto.customer!r} не найден."
            logger.info(msg)
            raise UserNotFoundError(msg)
        except InactiveUserError:
            msg = f"Ошибка: {create_user_dto.customer!r} не активен."
            logger.info(msg)
            raise InactiveUserError(msg)
        except ApplicationError as e:
            logger.critical("Ошибка логики создания нового пользователя: %r", e)
            raise
        if not customer_entity.is_superuser:
            msg = f"У {customer_entity.username!r} нет прав для создания пользователей."
            logger.warning(msg)
            raise UserPermissionsError(msg)
        try:
            UserEntityBusinessRules.check_username_and_password(
                username=create_user_dto.username,
                password=create_user_dto.password,
            )
        except InvalidValueToSetError as e:
            logger.info("%s: %r", e, create_user_dto.password)
            raise
        user_already_exists: UserEntity = (
            await self.get_user_use_case.get_user_by_username_or_none(
                create_user_dto.username
            )
        )
        if user_already_exists:
            msg = f"Пользователь с username={user_already_exists.username}(id={user_already_exists.id}) существует."
            logger.warning(msg)
            raise UserAlreadyExistsError(msg)

        entity: UserEntity = self.user_factory.create_new(
            firstname=create_user_dto.firstname,
            lastname=create_user_dto.lastname,
            username=create_user_dto.username,
            password=hash_password(create_user_dto.password),
            email=create_user_dto.email,
            organization=Organizations(create_user_dto.organization),
            is_active=create_user_dto.is_active,
            role=Roles(create_user_dto.role),
            phone_number=create_user_dto.phone_number,
            telegram=create_user_dto.telegram,
            description=create_user_dto.description,
        )

        logger.warning(entity)
        try:
            new_user_entity = await self.user_repository.add_user(entity)
            assert new_user_entity == entity
        except Exception as e:
            msg = f"Ошибка логики приложения при добавлении пользователя в репозиторий: {e}"
            logger.critical(msg)
            raise ApplicationError(msg)
        logger.info("Успешно создан новый пользователь: %r", new_user_entity)
        return new_user_entity
