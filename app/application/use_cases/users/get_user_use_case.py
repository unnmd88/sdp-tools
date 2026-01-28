import logging
from dataclasses import dataclass

from app_logging.dev.config import USERS_LOGGER

from domain.entities.user import UserEntity
from domain.exceptions import DomainEntityNotFoundError
from domain.repositories.users_repo_interface import UsersRepositoryProtocol

logger = logging.getLogger(USERS_LOGGER)


@dataclass(frozen=True, slots=True, kw_only=True)
class GetUserUseCaseImpl:
    user_repository: UsersRepositoryProtocol

    async def get_user_by_username_or_none(self, username: str) -> UserEntity | None:
        return await self.user_repository.get_by_username(username)

    async def get_user_by_username_or_raise(self, username: str) -> UserEntity:
        user: (
            UserEntity | None
        ) = await self.user_repository.get_by_username(username)
        if user is None:
            raise DomainEntityNotFoundError(
                message=f"Пользователь {username!r} не найден."
            )
        return user

    async def get_active_user_or_raise(self, username: str) -> UserEntity:
        user = await self.get_user_by_username_or_raise(username)
        if not user.is_active:
            raise DomainInactiveUserError(
                message=f"Пользователь {username!r} не активен."
            )
        return user


# @dataclass(frozen=True, slots=True, kw_only=True)
# class UsersAdministration:
#
#     repository: UsersRepositoryProtocol
#
#     async def get_user(self, username: str):
#         user: UserEntity | None = await self.repository.get_user_by_id_or_username_or_none(username)
#         if user is None:
#             raise UserNotFoundError
#
#     async def get_all_users(self, customer_username: str) -> Sequence[UserEntity]:
#         """
#         Получить всех пользователей системы.
#         :param customer_username: Username администратора, который делает запрос пользователей.
#         :return: Список всех пользователей системы
#         """
#         try:
#             customer: UserEntity = await self.repository.get_user_by_id_or_username_or_none(customer_username)
#         except UserNotFoundError:
#             logger.warning('Пользователь-администратор %r не найден.', customer_username)
#             raise UserAdministratorNotFoundError
#
#         if not customer.permissions.has(Permissions.READ_USERS):
#             logger.warning('Пользователю %r запрещен доступ к данным других пользователей.', customer.username)
#             raise UserPermissionsError
#         return await self.repository.get_many()
