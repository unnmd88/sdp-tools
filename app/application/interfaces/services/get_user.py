from typing import Protocol

from application.interfaces.repositories.users import UsersCrudRepositoryProtocol
from core.users._schemas import UserFromDbFullSchema


class UsersRepositoryProtocol(Protocol):
    # repository_factory: type[UsersRepositoryProtocol]

    async def get_user_by_username_or_none(self, name: str) -> UserFromDbFullSchema: ...

    async def get_user_by_id_or_none(self, user_id: int) -> UserFromDbFullSchema: ...
