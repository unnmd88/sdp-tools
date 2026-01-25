from dataclasses import dataclass
from typing import Protocol

from application.interfaces.repositories.users_repo_interface import (
    UsersRepositoryProtocol,
)
from application.interfaces.services.password_service_interface import PasswordServiceProtocol
from infrastructure.auth.jwt.jwt_service import BaseJWTService
from domain.dto.auth import UserAuthDTO
from domain.dto.jwt_dto import TokenDataDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class UserLoginAndIssueJWTUseCaseProtocol(Protocol):
    user_repository: UsersRepositoryProtocol
    user_password_service: type[PasswordServiceProtocol]
    jwt_service: BaseJWTService

    async def __call__(self, auth_data: UserAuthDTO) -> TokenDataDTO: ...
