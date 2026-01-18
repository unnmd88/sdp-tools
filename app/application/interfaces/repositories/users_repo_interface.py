from application.interfaces.repositories.base_repo_interface import BaseCrudProtocol
from domain.users.entities.user import UserEntity


class UsersRepositoryProtocol(BaseCrudProtocol):
    # async def get_user_by_username_or_none(self, username: str): ...

    async def get_user_by_id_or_username_or_none(
        self, username_or_id: str | int
    ) -> UserEntity: ...

    async def add_user(self, entity: UserEntity) -> UserEntity: ...
