from typing import Protocol

from application.dto.auth import UserAuthDTO
from domain.users.user_entity import UserEntity


class AuthServiceProtocol(Protocol):
    async def authenticate(self, auth_dto: UserAuthDTO) -> UserEntity: ...
