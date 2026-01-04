from collections.abc import Sequence

from application.interfaces.services.users import UsersServiceProtocol

from core.dto.users import CreateUserDTO, UpdateUserDTO, SearchUserDTO, SearchUsersDTO, ChangeUserPasswordDTO

from core.users.entities.user import UserEntity


class UsersCrudUseCaseImpl:
    def __init__(
        self,
        user_service: UsersServiceProtocol
    ):
        self.user_service = user_service

    async def get_user_by_username_or_id(self, user_dto: SearchUserDTO) -> UserEntity:
        return await self.user_service.get_user_by_username_or_id(user_dto)

    async def get_all_users(self, users_dto: SearchUsersDTO) -> Sequence[UserEntity]:
        return await self.user_service.get_all_users(users_dto)

    async def create_user(self, user: CreateUserDTO) -> UserEntity:
        return await self.user_service.create_user(user)

    async def update_user(self, user: UpdateUserDTO) -> UserEntity:
        return await self.user_service.update_user(user)

    async def change_password(self, dto: ChangeUserPasswordDTO) -> ChangeUserPasswordDTO:
        return await self.user_service.change_password(dto)