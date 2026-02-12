import logging
from dataclasses import dataclass
from typing import ClassVar

from app_logging.dev.config import USERS_LOGGER
from application.dto.users_dto import (
    ChangeUserPasswordByAdminDTO,
    ChangedUserPasswordByAdminDTO,
)
from application.exceptions import (
    ApplicationLayerError,
    PermissionDeniedError,
)
from application.interfaces import UserServiceProtocol, PasswordServiceProtocol
from domain.exceptions import DomainEntityNotFoundError
from domain.kernel.enums.unsorted import Roles
from domain.users.user_entity import UserEntity
from domain.value_objects.set_password_vo import SetPasswordVO

logger = logging.getLogger(USERS_LOGGER)


@dataclass(frozen=True, slots=True, kw_only=True)
class ResetUserPasswordByAdminUseCaseImpl:
    require_roles: ClassVar[frozenset[Roles]] = frozenset(
        [Roles.ADMIN, Roles.SUPERUSER, Roles.DIRECTOR]
    )

    user_service: UserServiceProtocol
    password_service: PasswordServiceProtocol

    async def __call__(
        self, reset_password_dto: ChangeUserPasswordByAdminDTO
    ) -> ChangedUserPasswordByAdminDTO:
        logger.info(
            "Запрос на смену пароля от пользователя с id=%r",
            reset_password_dto.customer_id,
        )

        customer = await self.user_service.get_active_user_by_id(
            reset_password_dto.customer_id
        )
        logger.info("Пользователь-заказчик c username=%r найден.", customer.username)

        if customer.role not in self.require_roles:
            logger.warning(
                "Ошибка доступа для пользователя %r. Текущая роль: %s. Требуется: %s",
                customer.username,
                customer.role,
                self.require_roles,
            )
            raise PermissionDeniedError

        subject = await self.user_service.try_get_user_by_username(
            reset_password_dto.subject_username
        )
        if subject is None:
            raise DomainEntityNotFoundError(
                public_message=f"Пользователь c username={reset_password_dto.subject_username} не найден."
            )

        new_password = SetPasswordVO.from_generated_password(
            subject=UserEntity.__name__
        ).password
        new_hashed_password = self.password_service.hash_password(new_password)
        await self.user_service.change_password(
            user_id=subject.id, hashed_password=new_hashed_password
        )
        updated_subject = await self.user_service.get_user_by_id(subject.id)
        if not self.password_service.verify_password(
            password=new_password,
            hashed_password=updated_subject.password,
        ):
            exc = ApplicationLayerError(
                private_message="Ошибка логики обновления пароля."
            )
            logger.error(exc.to_dict())
            raise exc
        logger.info("Пароль пользователя %r успешно изменён.", customer.username)
        return ChangedUserPasswordByAdminDTO(
            username=updated_subject.username, new_password=new_password
        )
