from typing import Protocol

from application.dto.auth import UserAuthDTO
from domain.entities import UserEntity


class AuthServiceProtocol(Protocol):
    async def authenticate(self, auth_dto: UserAuthDTO) -> UserEntity: ...
