from collections.abc import Sequence

from application.interfaces.services.authentication import AuthenticationSchemaProtocol
from application.interfaces.services.users_crud import (
    UsersServiceProtocol,
)

from core.dto.tokens import TokenDataDTO
from core.dto.users import CreateUserDTO, UpdateUserDTO, SearchUserByIdDTO, SearchUsersDTO

from core.users.entities.user import UserEntity


class UsersCrudUseCaseImpl:
    def __init__(
        self,
        user_service: UsersServiceProtocol
    ):
        self.user_service = user_service

    async def get_user_by_id(self, user_dto: SearchUserByIdDTO) -> UserEntity:
        return await self.user_service.get_user_by_id_or_none(user_dto)

    async def get_all_users(self, users_dto: SearchUsersDTO) -> Sequence[UserEntity]:
        return await self.user_service.get_all_users(users_dto)

    async def create_user(self, user: CreateUserDTO) -> UserEntity:
        return await self.user_service.create_user(user)

    async def update_user(self, user: UpdateUserDTO) -> UserEntity:
        return await self.user_service.update_user(user)