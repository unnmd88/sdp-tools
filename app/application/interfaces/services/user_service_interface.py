from typing import Protocol

from application.dto.users import UserDTO
from domain.entities import UserEntity


class UserReadServiceProtocol(Protocol):
    async def get_user_by_username(self, username: str) -> UserEntity | None: ...
    async def get_user_by_id(self, id: int) -> UserEntity | None: ...


class UserWriteServiceProtocol(Protocol):
    async def update_user(self, user_id: int, update_data) -> UserEntity: ...
    async def change_password(
        self, user_id: int, current_password: str, new_password: str
    ) -> None: ...


class UserServiceProtocol(
    UserReadServiceProtocol, UserWriteServiceProtocol, Protocol
): ...
