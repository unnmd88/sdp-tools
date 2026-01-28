from typing import Protocol

from application.dto.auth import UserAuthDTO
from application.dto.users import UserDTO


class AuthServiceProtocol(Protocol):

    async def authenticate(self, auth_dto: UserAuthDTO) -> UserDTO | None: ...

