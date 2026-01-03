from typing import Protocol, Sequence

from application.interfaces.repositories.users import UsersRepositoryProtocol
from application.interfaces.services.authentication import AuthenticationSchemaProtocol
from core.dto.users import CreateUserDTO, UpdateUserDTO, SearchUserDTO, SearchUsersDTO, ChangeUserPasswordDTO
from core.users.entities.user import UserEntity


class UsersServiceProtocol(Protocol):

    def __init__(
        self,
        repository: UsersRepositoryProtocol,
    ):
        self.repository = repository

    async def authenticate(self, auth_data: AuthenticationSchemaProtocol) -> UserEntity: ...

    async def get_user_by_username_or_id(self, search_dto: SearchUserDTO) -> UserEntity: ...

    async def get_all_users(self, users_dto: SearchUsersDTO) -> Sequence[UserEntity]: ...

    async def create_user(self, user: CreateUserDTO) -> UserEntity: ...

    async def update_user(self, user: UpdateUserDTO) -> UserEntity: ...

    async def change_password(self, dto: ChangeUserPasswordDTO) -> UserEntity: ...
