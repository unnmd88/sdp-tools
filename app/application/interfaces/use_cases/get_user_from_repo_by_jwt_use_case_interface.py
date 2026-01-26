from dataclasses import dataclass
from typing import Protocol

from application.interfaces.services.get_user_from_repo_by_jwt_service_interface import (
    GetUserFromRepoByJWTServiceProtocol,
)
from domain.dto.users import UserDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class GetUserFromRepoByJWTUseCaseProtocol(Protocol):
    service: GetUserFromRepoByJWTServiceProtocol

    async def __call__(self, access_token: str) -> UserDTO: ...
