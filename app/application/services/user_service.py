import logging
from dataclasses import dataclass

from app_logging.dev.config import DOMAIN
from application.exceptions import InactiveAccountError
from application.utils import async_handle_corrupted_data_in_repo
from domain.entities import UserEntity
from domain.exceptions import DomainEntityNotFoundError
from domain.repositories.users_repo_interface import UsersRepositoryProtocol

logger = logging.getLogger(DOMAIN)


@dataclass(frozen=True, slots=True, kw_only=True)
class UserServiceImpl:
    user_repository: UsersRepositoryProtocol

    @async_handle_corrupted_data_in_repo(logger=logger)
    async def get_user_by_username(self, username: str) -> UserEntity | None:
        return await self.user_repository.get_by_username(username)

    @async_handle_corrupted_data_in_repo(logger=logger)
    async def get_user_by_id(self, _id: int) -> UserEntity | None:
        return await self.user_repository.get_by_id(_id)

    async def get_user_by_id_or_raise(self, _id: int) -> UserEntity:
        if (user := await self.get_user_by_id(_id)) is None:
            raise DomainEntityNotFoundError(public_message=f"Пользователь не найден.")
        return user

    async def get_active_user_by_id_or_raise(self, _id: int) -> UserEntity:
        if (user := await self.get_user_by_id(_id)) is None:
            raise DomainEntityNotFoundError(public_message=f"Пользователь не найден.")
        if not user.is_active:
            raise InactiveAccountError(public_message=f"Пользователь не активен.")
        return user

    async def change_password(
        self, user_id: int, hashed_password: bytes
    ) -> UserEntity | None:
        return await self.user_repository.change_password(user_id, hashed_password)

    async def add_new_user(self, user_data: UserEntity) -> UserEntity:
        return await self.user_repository.add(user_data)

    @async_handle_corrupted_data_in_repo(logger=logger)
    async def get_user_by_filters(self, **filters) -> UserEntity | None:
        return await self.user_repository.get_user_by_filters(**filters)
