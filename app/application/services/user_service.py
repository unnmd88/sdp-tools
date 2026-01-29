from dataclasses import dataclass

from application.dto.users import UserDTO
from domain.repositories.users_repo_interface import UsersRepositoryProtocol

#
# @dataclass(frozen=True, slots=True, kw_only=True)
# class UserServiceImpl:
#
#     user_repository: UsersRepositoryProtocol
#
#     async def get_user_by_username(self, username: str) -> UserDTO | None:
#         user_entity = await self.user_repository.get_user_by_id_or_username_or_none(username)
#         return UserDTO.from_entity(user_entity) if user_entity else None