import logging
from dataclasses import dataclass

from app_logging.dev.config import USERS_LOGGER
from application.interfaces.repositories.users_repo_interface import (
    UsersRepositoryProtocol,
)
from application.interfaces.use_cases.get_user_use_case_interface import (
    GetUserUseCaseProtocol,
)
from domain.dto.common import ToUpdateRecordDTO
from domain.dto.users import ChangeUserPasswordDTO
from domain.exceptions.base import ApplicationError
from domain.users.entities.user import UserEntity
from domain.users.exceptions import (
    UserNotFoundError,
    InactiveUserError,
    InvalidUsernameOrPasswordError,
    InvalidUsernameOrPasswordToSetError,
)
from domain.services.user_password_service import hash_password
from domain.services.field_values_constraints import (
    password_validator,
)

logger = logging.getLogger(USERS_LOGGER)


@dataclass(frozen=True, slots=True, kw_only=True)
class ChangeUserPasswordUseCaseImpl:
    user_repository: UsersRepositoryProtocol
    get_user_use_case: GetUserUseCaseProtocol

    async def __call__(self, dto: ChangeUserPasswordDTO) -> ChangeUserPasswordDTO:
        logger.info("Запрос на смену пароля с username=%r", dto.subject)
        try:
            subject: UserEntity = await self.get_user_use_case.get_active_user_or_raise(
                dto.subject
            )
            logger.info("Пользователь найден: %r.", subject)
        except UserNotFoundError:
            logger.info("Пользователь %r не найден.", dto.subject)
            raise
        except InactiveUserError:
            logger.warning("Ошибка: пользователь %r не активен.", dto.subject)
            raise
        if not subject.validate_password(dto.old_password):
            logger.warning("Ошибка: неверный пароль пользователя %r.", subject.username)
            raise InvalidUsernameOrPasswordError
        if not password_validator(dto.new_password):
            msg = "Ошибка: Недопустимый пароль"
            logger.info("%s: %r", msg, dto.new_password)
            raise InvalidUsernameOrPasswordToSetError(f"{msg}.")
        if subject.password == subject.username:
            msg = "Ошибка: username и пароль должны отличаться"
            logger.info(
                "%s: username=%r, пароль=%r", msg, subject.username, subject.password
            )
            raise InvalidUsernameOrPasswordToSetError(msg)
        update_dto = ToUpdateRecordDTO(
            search_criteria={"id": subject.id},
            fields={"password": hash_password(dto.new_password)},
        )
        logger.info("Меняю пароль у пользователя username=%r", subject.username)
        updated_dto = await self.user_repository.update_one(
            update_record_dto=update_dto
        )

        updated_entity: UserEntity = updated_dto.new
        if not updated_entity.validate_password(dto.new_password):
            msg = "!!! Ошибка логики обновления пароля."
            logger.critical(msg)
            raise ApplicationError(msg)
        logger.info("Пароль успешно изменён.")
        return ChangeUserPasswordDTO(
            subject=subject.username,
            old_password=dto.old_password,
            new_password=dto.new_password,
        )
