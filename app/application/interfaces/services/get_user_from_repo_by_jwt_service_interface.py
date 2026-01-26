from dataclasses import dataclass
from typing import Protocol

from application.interfaces.repositories.users_repo_interface import (
    UsersRepositoryProtocol,
)
from domain.enums.unsorted import Roles
from domain.users.entities.user import UserEntity
from infrastructure.auth.jwt.jwt_service import BaseJWTService


@dataclass(frozen=True, slots=True, kw_only=True)
class GetUserFromRepoByJWTServiceProtocol(Protocol):
    user_repository: UsersRepositoryProtocol
    jwt_service: BaseJWTService
    require_role: Roles | None
    require_active: bool

    async def __call__(self, token: str) -> UserEntity: ...
