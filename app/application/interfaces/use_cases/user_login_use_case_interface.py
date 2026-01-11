from dataclasses import dataclass
from typing import Protocol

from application.interfaces.repositories.users_repo_interface import (
    UsersRepositoryProtocol,
)
from core.dto.auth import UserAuthDTO
from core.users.entities.user import UserEntity


@dataclass(frozen=True, slots=True, kw_only=True)
class UserLoginUseCaseProtocol(Protocol):
    user_repository: UsersRepositoryProtocol

    async def __call__(self, auth_data: UserAuthDTO) -> UserEntity: ...
