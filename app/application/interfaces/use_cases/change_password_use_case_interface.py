from dataclasses import dataclass
from typing import Protocol

from application.interfaces.repositories.users_repo_interface import (
    UsersRepositoryProtocol,
)
from application.interfaces.use_cases.get_user_use_case_interface import (
    GetUserUseCaseProtocol,
)
from domain.dto.users import ChangeUserPasswordDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class ChangeUserPasswordUseCaseProtocol(Protocol):
    user_repository: UsersRepositoryProtocol
    get_user_use_case: GetUserUseCaseProtocol

    async def __call__(self, dto: ChangeUserPasswordDTO) -> ChangeUserPasswordDTO: ...
