import asyncio
import logging
import os
from dataclasses import dataclass

from app_logging.dev.config import USERS_LOGGER
from application.dto.users import UserDTO
from application.exceptions import AuthenticationError
from application.interfaces import PasswordServiceProtocol
from domain.entities import UserEntity
from domain.enums.attrs_names import PublicAttrNamesEnum
from domain.enums.unsorted import Roles, Organizations
from domain.enums.validation_err_messages import ErrorMessages
from domain.exceptions import DomainEntityAlreadyExistsError, DomainError
from domain.repositories.users_repo_interface import UsersRepositoryProtocol
from infrastructure.auth.password_service import BcryptPasswordService
from infrastructure.database.api import db_api
from infrastructure.database.user_reposirory import UsersSqlAlchemyRepository

logger = logging.getLogger(USERS_LOGGER)
from dotenv import load_dotenv

load_dotenv(".env.dev")

@dataclass(frozen=True, slots=True, kw_only=True)
class CreateDirectorUseCase:
    user_repository: UsersRepositoryProtocol
    password_service: PasswordServiceProtocol

    async def __call__(
        self,
        *,
        secret_key: str,
        username: str = os.getenv("DIRECTOR_USERNAME"),
        password: str = os.getenv("DIRECTOR_PASSWORD"),
        email: str | None = None,
        first_name: str = "Director",
        last_name: str = "Director",
    ):

        if (secret_key_from_env := os.getenv("SECRET_KEY_TO_CREATE_DIRECTOR")) is None:
            logger.warning("SECRET_KEY_TO_CREATE_DIRECTOR не найден в переменных окружения")
            raise DomainError(private_message="SECRET_KEY_TO_CREATE_DIRECTOR не найден в переменных окружения")
        if not isinstance(secret_key, str):
            logger.warning("Неверный тип секретного ключа. Ожидается строка. Передано: %r", type(secret_key))
            raise DomainError(
                private_message=f"Неверный тип секретного ключа. Ожидается строка. Передано: {type(secret_key)}")
        if secret_key != secret_key_from_env:
            raise AuthenticationError(private_message="Неверный секретный ключ")

        already_exist = await self.user_repository.get_by_username(username)
        if already_exist:
            raise DomainEntityAlreadyExistsError(
                private_message=ErrorMessages.already_exists.format(
                    "Пользователь",
                    str(PublicAttrNamesEnum.username),
                    username,
                )
            )
        director_entity = UserEntity(
            id=None,
            username=username,
            password=self.password_service.hash_password(password),
            email=email,
            firstname=first_name,
            lastname=last_name,
            role=Roles.director,
            organization=Organizations.SDP,
            is_active=True,
            phone_number=None,
            telegram=None,
            description="Корневой пользователь системы",
        )
        await self.user_repository.add(director_entity)
        return UserDTO.from_entity(director_entity)


async def main():
    async with db_api.session_factory() as session:
        user_repo = UsersSqlAlchemyRepository(session=session)
        use_case = CreateDirectorUseCase(
            user_repository=user_repo,
            password_service=BcryptPasswordService(),
        )
        await use_case(secret_key="12345")




if __name__ == "__main__":

    asyncio.run(main())


