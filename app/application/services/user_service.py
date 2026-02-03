import logging
from dataclasses import dataclass

from app_logging.dev.config import DOMAIN
from application.utils import async_handle_corrupted_data_in_repo
from domain.entities import UserEntity
from domain.repositories.users_repo_interface import UsersRepositoryProtocol

logger = logging.getLogger(DOMAIN)


@dataclass(frozen=True, slots=True, kw_only=True)
class UserServiceImpl:

    user_repository: UsersRepositoryProtocol

    @async_handle_corrupted_data_in_repo(logger=logger)
    async def get_user_by_username(self, username: str) -> UserEntity | None:
        return await self.user_repository.get_by_username(username)
