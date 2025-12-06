from collections.abc import Sequence

from application.dtos.users import CreateUserDTO
from application.interfaces.services.users_crud import (
    UsersServiceProtocol,
)
from core.users.entities.user import UserEntity


class UsersCrudUseCaseImpl:
    def __init__(self, user_service: UsersServiceProtocol):
        self.user_service = user_service

    async def get_user_by_username(self, username: str) -> UserEntity:
        return await self.user_service.get_user_by_username_or_none(username)

    async def get_user_by_id(self, user_id: int) -> UserEntity:
        return await self.user_service.get_user_by_id_or_none(user_id)

    async def get_all_users(self) -> Sequence[UserEntity]:
        return await self.user_service.get_all_users()

    async def create_user(self, user: CreateUserDTO) -> UserEntity:
        return await self.user_service.create_user(user)
