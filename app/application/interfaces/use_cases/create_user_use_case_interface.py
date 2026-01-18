from dataclasses import dataclass
from typing import Protocol

from application.interfaces.use_cases.get_user_use_case_interface import (
    GetUserUseCaseProtocol,
)

from domain.dto.users import CreateUserDTO
from domain.users.entities.user import UserEntity


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateUserUseCaseProtocol(Protocol):
    get_user_use_case: GetUserUseCaseProtocol

    async def __call__(self, create_user_dto: CreateUserDTO) -> UserEntity: ...
