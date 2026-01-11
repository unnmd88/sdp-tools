from dataclasses import dataclass
from typing import Protocol

from application.interfaces.repositories.users_repo_interface import (
    UsersRepositoryProtocol,
)
from core.users.entities.user import UserEntity


@dataclass(frozen=True, slots=True, kw_only=True)
class GetUserUseCaseProtocol(Protocol):
    user_repository: UsersRepositoryProtocol

    async def get_user_by_username_or_none(
        self, username: str
    ) -> UserEntity | None: ...

    async def get_user_by_username_or_raise(self, username: str) -> UserEntity: ...

    async def get_active_user_or_raise(self, username: str) -> UserEntity: ...
