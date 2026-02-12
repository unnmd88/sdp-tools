import logging
from dataclasses import dataclass

from app_logging.dev.config import USERS_LOGGER
from application.dto.users_dto import ChangeUserPasswordDTO
from application.exceptions import AuthenticationError, ApplicationLayerError
from application.interfaces import UserServiceProtocol, PasswordServiceProtocol
from application.interfaces.uow_interface import UnitOfWorkProtocol
from domain.kernel.enums.validation_err_messages import ErrorMessages
from domain.users.user_entity import UserEntity
from domain.value_objects.set_password_vo import SetPasswordVO

logger = logging.getLogger(USERS_LOGGER)


@dataclass(frozen=True, slots=True, kw_only=True)
class ChangeUserPasswordUseCaseImpl:
    uow: UnitOfWorkProtocol
    user_service: UserServiceProtocol
    password_service: PasswordServiceProtocol

    async def __call__(
        self, user_id, change_password_dto: ChangeUserPasswordDTO
    ) -> ChangeUserPasswordDTO:
        logger.info("Запрос на смену пароля с id=%r", user_id)
        async with self.uow:
            user = await self.user_service.get_active_user_by_id(user_id)
            logger.info("Пользователь c username=%r найден.", user.username)
            if not self.password_service.verify_password(
                password=change_password_dto.old_password,
                hashed_password=user.password,
            ):
                logger.info("Неверный пароль для пользователя %r.", user.username)
                raise AuthenticationError(
                    private_message=ErrorMessages.invalid_username_or_password
                )
            hashed_password = self.password_service.hash_password(
                SetPasswordVO(
                    subject=UserEntity.__name__,
                    password=change_password_dto.new_password,
                ).password
            )
            await self.user_service.change_password(
                user_id=user_id, hashed_password=hashed_password
            )
            user = await self.user_service.get_user_by_id(user.id)
            if not self.password_service.verify_password(
                password=change_password_dto.new_password,
                hashed_password=user.password,
            ):
                raise ApplicationLayerError(
                    private_message="Ошибка логики обновления пароля."
                )
            logger.info("Пароль пользователя %r успешно изменён.", user.username)
        return change_password_dto
