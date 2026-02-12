import logging
from collections.abc import Container, Callable, Awaitable
from dataclasses import dataclass

from app_logging.dev.config import DOMAIN
from application.exceptions import InactiveAccountError, PermissionDeniedError
from application.utils import async_handle_corrupted_data_in_repo
from domain.exceptions import DomainEntityNotFoundError
from domain.kernel.enums.unsorted import Roles
from domain.repositories.users_repo_interface import UsersRepositoryProtocol
from domain.users.user_entity import UserEntity

logger = logging.getLogger(DOMAIN)


@dataclass(frozen=True, slots=True, kw_only=True)
class UserServiceImpl:
    user_repository: UsersRepositoryProtocol

    @async_handle_corrupted_data_in_repo(logger=logger)
    async def try_get_user_by_filters(self, **filters) -> UserEntity | None:
        return await self.user_repository.get_user_by_filters(**filters)

    @async_handle_corrupted_data_in_repo(logger=logger)
    async def try_get_user_by_username(self, username: str) -> UserEntity | None:
        return await self.user_repository.get_by_username(username)

    @async_handle_corrupted_data_in_repo(logger=logger)
    async def try_get_user_by_id(self, user_id: int) -> UserEntity | None:
        return await self.user_repository.get_by_id(user_id)

    async def _get_user_with_checks(
        self,
        fetch_method: Callable | Awaitable,
        identifier: str | int,
        *,
        raise_if_not_found: bool = False,
        require_is_active: bool = False,
        allowed_roles: Container[Roles] = None,
        identifier_label: str = "",
        action: str = "",
    ) -> UserEntity | None:
        """
        Обертка для получения пользователя с проверками.

        Args:
            fetch_method: Метод для получения пользователя
            identifier: id, username и т.д.
            identifier_label: Для сообщений об ошибках ("ID", "username")
            raise_if_not_found: Бросить исключение если не найден
            require_is_active: Проверять активность
            allowed_roles: Проверять роли

        Returns:
            UserEntity если найден и прошел проверки
            None если не найден и raise_if_not_found=False
        """
        user = await fetch_method(identifier)
        if user is None:
            if raise_if_not_found:
                raise DomainEntityNotFoundError(
                    public_message=f"Пользователь c {identifier_label}={identifier} не найден."
                )
            else:
                return None

        if require_is_active and not user.is_active:
            raise InactiveAccountError(
                public_message=f"Пользователь c {identifier_label}={identifier} не активен."
            )
        if allowed_roles is not None and user.role not in allowed_roles:
            raise PermissionDeniedError(
                public_message=(
                    f"Не удалось выполнить операцию: {action}. "
                    f"У пользователя c {identifier_label}={identifier} нет прав."
                )
            )
        return user

    async def get_user_by_id(
        self,
        user_id: int,
    ) -> UserEntity:
        return await self._get_user_with_checks(
            fetch_method=self.try_get_user_by_id,
            identifier=user_id,
            raise_if_not_found=True,
            identifier_label="ID",
        )

    async def get_active_user_by_id(self, user_id: int) -> UserEntity:
        return await self._get_user_with_checks(
            fetch_method=self.try_get_user_by_id,
            identifier=user_id,
            raise_if_not_found=True,
            require_is_active=True,
            identifier_label="ID",
        )

    async def get_active_user_by_id_and_check_role(
        self,
        *,
        user_id: int,
        allowed_roles: Container[Roles],
        action: str = "",
    ) -> UserEntity:
        return await self._get_user_with_checks(
            fetch_method=self.try_get_user_by_id,
            identifier=user_id,
            raise_if_not_found=True,
            allowed_roles=allowed_roles,
            require_is_active=True,
            identifier_label="ID",
            action=action,
        )

    async def verify_user_is_active(
        self,
        user_id: int,
        action: str = "",
    ) -> None:
        """Проверить что пользователь активен"""
        await self._get_user_with_checks(
            fetch_method=self.try_get_user_by_id,
            identifier=user_id,
            raise_if_not_found=True,
            require_is_active=True,
            allowed_roles=None,
            identifier_label="ID",
            action=action,
        )

    async def verify_user_is_active_and_has_roles(
        self,
        user_id: int,
        required_roles: Container[Roles],
        action: str = "",
    ) -> None:
        """
        Проверить что пользователь активен и имеет нужные роли.

        Args:
            action: Действие для сообщения об ошибке
            user_id: ID пользователя для проверки
            required_roles: Требуемые роли (хотя бы одну)

        Raises:
            DomainEntityNotFoundError: Пользователь не найден
            InactiveAccountError: Пользователь не активен
            PermissionDeniedError: Не имеет нужных ролей
        """
        await self._get_user_with_checks(
            fetch_method=self.try_get_user_by_id,
            identifier=user_id,
            raise_if_not_found=True,
            require_is_active=True,
            allowed_roles=required_roles,
            identifier_label="ID",
            action=action,
        )

    async def change_password(
        self, user_id: int, hashed_password: bytes
    ) -> UserEntity | None:
        return await self.user_repository.change_password(user_id, hashed_password)

    async def add_new_user(self, user_data: UserEntity) -> UserEntity:
        return await self.user_repository.add(user_data)
