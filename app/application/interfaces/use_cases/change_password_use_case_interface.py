from dataclasses import dataclass
from typing import Protocol

from application.interfaces.repositories.users_repo_interface import (
    UsersRepositoryProtocol,
)
from application.interfaces.services.get_user_from_repo_by_jwt_service_interface import (
    GetUserUseCaseProtocol,
)
from domain.dto.users import ChangeUserPasswordDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class ChangeUserPasswordUseCaseProtocol(Protocol):
    user_repository: UsersRepositoryProtocol
    get_user_use_case: GetUserUseCaseProtocol

    async def __call__(self, dto: ChangeUserPasswordDTO) -> ChangeUserPasswordDTO: ...
