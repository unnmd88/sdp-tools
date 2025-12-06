from application.dtos.users import CreateUserDTO
from application.interfaces.repositories.base import BaseCrudProtocol


class UsersRepositoryProtocol(BaseCrudProtocol):
    async def get_user_by_username_or_none(self, username: str): ...

    async def create_user(self, user): ...
