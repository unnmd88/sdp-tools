import logging
from collections.abc import Container, Callable, Awaitable
from dataclasses import dataclass
from typing import Any

from app_logging.dev.config import DOMAIN
from application.exceptions import InactiveAccountError, PermissionDeniedError
from application.helpers.entity_fetcher import EntityFetcher
from application.interfaces.services.user_service_interface import UserReadServiceProtocol
from application.use_cases.users.admin.commands import CreateUserCommand
from application.use_cases.users.commands import ChangeUserPasswordCommand
from domain.exceptions import DomainEntityNotFoundError, DomainEntityAlreadyExistsError
from domain.kernel.enums.attrs_names import PublicAttrNamesEnum
from domain.kernel.enums.unsorted import Roles
from domain.kernel.enums.validation_err_messages import ErrorMessages
from domain.repositories.users_repo_interface import UsersReadRepositoryProtocol
from domain.users.user_entity import UserEntity

logger = logging.getLogger(DOMAIN)


@dataclass(frozen=True, slots=True, kw_only=True)
class BaseReadUserServiceImpl:
    user_repository: UsersReadRepositoryProtocol

    # async def _get_user_with_checks(
    #     self,
    #     fetch_method: Callable | Awaitable,
    #     fetch_method_arg_criteria: Any,
    #     *,
    #     raise_if_not_found: bool = False,
    #     require_is_active: bool = False,
    #     allowed_roles: Container[Roles] = None,
    #     public_message_if_not_found: str = str(ErrorMessages.user_not_found),
    #     public_message_if_not_active: str = str(ErrorMessages.inactive_user_please_contact_support),
    #     public_message_if_not_allowed: str = str(ErrorMessages.permission_denied),
    # ) -> UserEntity | None:
    #     """
    #     Обертка для получения пользователя с проверками.
    #
    #     Args:
    #         fetch_method: Метод для получения пользователя
    #         fetch_method_arg_criteria: id, username и т.д.
    #         identifier_label: Для сообщений об ошибках ("ID", "username")
    #         raise_if_not_found: Бросить исключение если не найден
    #         require_is_active: Проверять активность
    #         allowed_roles: Проверять роли
    #
    #     Returns:
    #         UserEntity если найден и прошел проверки
    #         None если не найден и raise_if_not_found=False
    #     """
    #     user = await fetch_method(fetch_method_arg_criteria)
    #     if user is None:
    #         if raise_if_not_found:
    #             raise DomainEntityNotFoundError(public_message=public_message_if_not_found)
    #         else:
    #             return None
    #     if require_is_active and not user.is_active:
    #         raise InactiveAccountError(
    #             public_message=public_message_if_not_active
    #         )
    #     if allowed_roles is not None and user.role not in allowed_roles:
    #         raise PermissionDeniedError(public_message=public_message_if_not_allowed)
    #     return user

    # async def get_by_username(
    #     self,
    #     username: str,
    # ) -> UserEntity:
    #     return await self.fetcher.fetch(
    #         fetch_method=self.user_repository.try_by_username,
    #         fetch_method_arg_criteria=username,
    #         raise_if_not_found=True,
    #         public_message_if_not_found=ErrorMessages.user_with_attr_not_found.format(
    #             PublicAttrNamesEnum.username, username
    #         ),
    #     )
    #
    # async def try_by_username(
    #     self,
    #     username: str,
    # ) -> UserEntity | None:
    #     return await self.user_repository.try_by_username(username)

    async def try_by_username(
        self,
        username: str,
    ) -> UserEntity | None:
        return await self.user_repository.try_by_username(username)

    async def get_by_username(
        self,
        username: str,
    ) -> UserEntity:
        if (user := await self.try_by_username(username)) is None:
            raise DomainEntityNotFoundError(
                public_message=ErrorMessages.user_with_attr_not_found.format(
                    f"{str(PublicAttrNamesEnum.username)!r}", username
                )
            )
        return user

    async def try_by_id(
        self,
        user_id: int,
    ) -> UserEntity | None:
        return await self.user_repository.try_by_id(user_id)

    async def get_by_id(
            self,
            user_id: int,
    ) -> UserEntity:
        if (user := await self.user_repository.try_by_id(user_id)) is None:
            raise DomainEntityNotFoundError(
                public_message=ErrorMessages.user_with_attr_not_found.format(
                    f"{str(PublicAttrNamesEnum.id.upper())!r}", user_id
                )
            )
        return user

    async def get_active_user_by_id(self, user_id: int) -> UserEntity:
        user = await self.get_by_id(user_id)
        if not user.is_active:
            if user.is_active:
                exc = InactiveAccountError()
                logger.warning(exc.to_dict())
                raise exc
        return user

    async def get_active_user_by_id_and_check_role(
        self,
        *,
        user_id: int,
        allowed_roles: Container[Roles],
        action: str = "",
    ) -> UserEntity:
        user = await self.get_active_user_by_id(user_id)
        if user.role not in allowed_roles:
            if action:
                exc = (
                    PermissionDeniedError(
                        public_message=ErrorMessages.permission_denied_for_this_action.format(action),
                        private_message=(
                            f"У пользователя {user_id} нет роли {allowed_roles} для выполнения действия {action}"
                        )
                    )
                    .with_entity_context(entity=UserEntity, entity_id=user_id)
                    .with_handler_context(
                        handler=f"{self.__class__.__name__} : {self.get_active_user_by_id_and_check_role.__name__}"
                    )
                    .with_action_context(action=action)
                )
                logger.warning(exc.to_dict())
                raise exc
        return user

    async def verify_user_is_active(
        self,
        user_id: int,
    ) -> None:
        """Проверить что пользователь активен"""
        await self.get_active_user_by_id(user_id)

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
        await self.get_active_user_by_id_and_check_role(
            user_id=user_id,
            allowed_roles=required_roles,
            action=action,
        )

@dataclass(frozen=True, slots=True, kw_only=True)
class UserUpdateServiceImpl:
    read_user_service: UserReadServiceProtocol

    async def change_password(
        self,
        user_id: int,
        old_password: str,
        new_password: str,
    ) -> UserEntity: ...


    # async def change_password(
    #     self, user_id: int, hashed_password: bytes
    # ) -> UserEntity | None:
    #     return await self.user_repository.change_password(user_id, hashed_password)

