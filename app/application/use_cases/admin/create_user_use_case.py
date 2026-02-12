import logging

from dataclasses import dataclass
from typing import ClassVar

from app_logging.dev.config import USERS_LOGGER
from application.dto.users_dto import CreateUserDTO, UserDTO
from application.exceptions import PermissionDeniedError
from application.interfaces import UserServiceProtocol

from application.interfaces.services.password_service_interface import (
    PasswordServiceProtocol,
)
from application.interfaces.uow_interface import UnitOfWorkProtocol
from domain.kernel.enums.unsorted import Roles

from domain.users.user_entity import UserEntity
from domain.exceptions import DomainEntityAlreadyExistsError
from domain.value_objects.set_password_vo import SetPasswordVO


logger = logging.getLogger(USERS_LOGGER)


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateUserUseCaseImpl:
    """Класс для создания нового пользователя системы."""

    require_roles: ClassVar[frozenset[Roles]] = frozenset(
        [Roles.SUPERUSER, Roles.DIRECTOR]
    )

    uow: UnitOfWorkProtocol
    user_service: UserServiceProtocol
    password_service: PasswordServiceProtocol

    async def __call__(self, create_user_dto: CreateUserDTO) -> UserDTO:
        logger.info(
            "Запрос на создание нового пользователя системы. Заказчик(id)=%r",
            create_user_dto.customer_id,
        )
        async with self.uow:
            customer = await self.user_service.get_user_by_id(
                create_user_dto.customer_id
            )
            logger.info("Заказчик c username=%r найден.", customer.username)
            if customer.role not in self.require_roles:
                logger.warning(
                    "Ошибка доступа для пользователя %r. Текущая роль: %s. Требуется: %s",
                    customer.username,
                    customer.role,
                    self.require_roles,
                )
                raise PermissionDeniedError
            logger.debug(
                "Право на создание пользователя у заказчика(%r) подтверждено.",
                customer.username,
            )
            logger.debug("Данные нового пользователя: %r", create_user_dto)

            existing_user = await self.user_service.try_get_user_by_username(
                create_user_dto.username
            )
            if existing_user is not None:
                logger.warning(
                    "Ошибка: пользователь с username=%r существует.",
                    create_user_dto.username,
                )
                raise DomainEntityAlreadyExistsError(
                    public_message=f"Пользователь с username={create_user_dto.username} уже существует."
                )
            logger.debug(
                "Право на создание пользователя с username=%r подтверждено.",
                create_user_dto.username,
            )
            if create_user_dto.email is not None:
                if (
                    await self.user_service.try_get_user_by_filters(
                        email=create_user_dto.email
                    )
                    is not None
                ):
                    logger.warning(
                        "Ошибка: пользователь с email=%r существует.",
                        create_user_dto.email,
                    )
                    raise DomainEntityAlreadyExistsError(
                        public_message=f"Пользователь с email={create_user_dto.email} уже существует."
                    )
                logger.debug(
                    "Право на создание пользователя с email=%r подтверждено.",
                    create_user_dto.email,
                )
            validated_password = SetPasswordVO(
                subject=UserEntity.__class__.__name__, password=create_user_dto.password
            ).password
            hashed_password = self.password_service.hash_password(validated_password)
            logger.debug(
                "Право на создание пользователя с указанным паролем подтверждено."
            )
            user_to_create = UserEntity.create_new_user(
                firstname=create_user_dto.firstname,
                lastname=create_user_dto.lastname,
                username=create_user_dto.username,
                password=hashed_password,
                email=create_user_dto.email,
                organization=create_user_dto.organization,
                is_active=create_user_dto.is_active,
                role=create_user_dto.role,
                phone_number=create_user_dto.phone_number,
                telegram=create_user_dto.telegram,
                description=create_user_dto.description,
            )
            logger.debug(
                "Валидация данных пользователя завершена. Сохранение в репозиторий..."
            )
            new_user = await self.user_service.add_new_user(user_to_create)
            logger.info(
                "Пользователь c id=%r и username=%r успешно сохранен в репозиторий.",
                new_user.id,
                new_user.username,
            )
        return UserDTO.from_entity(new_user)
