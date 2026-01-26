from dataclasses import dataclass

from application.interfaces.repositories.users_repo_interface import (
    UsersRepositoryProtocol,
)
from domain.enums.attrs_names import PublicAttrNamesEnum
from domain.enums.unsorted import Roles
from domain.enums.validation_err_messages import ErrorMessages
from domain._exceptions.entity_not_found_exc import DomainEntityNotFoundError
from domain._exceptions.permissions_exc import (
    DomainUserPermissionError,
    DomainInactiveUserError,
    DomainUnauthorizedError,
)
from domain.users.entities.user import UserEntity
from infrastructure.auth.exceptions import RottenTokenError
from infrastructure.auth.jwt.jwt_service import BaseJWTService


@dataclass(frozen=True, slots=True, kw_only=True)
class GetUserFromRepoByJWTService:
    user_repository: UsersRepositoryProtocol
    jwt_service: BaseJWTService = BaseJWTService()
    require_role: Roles | None = None
    require_active: bool = True

    async def __call__(self, token: str) -> UserEntity:
        try:
            decoded_token = self.jwt_service.decode_jwt(token=token)
        except RottenTokenError:
            raise DomainUnauthorizedError(message="Тестовое сообщение Invalid token")

        user: UserEntity = await self.user_repository.get_one_by_id_or_none(
            decoded_token.user_id
        )
        if user is None:
            raise DomainEntityNotFoundError(
                message=ErrorMessages.user_not_found.format(
                    str(PublicAttrNamesEnum.username),
                    decoded_token.sub,
                )
            )
        if user.username != decoded_token.sub:
            # TODO: Обязательно добавить логирование! Не должно быть такого
            raise DomainUnauthorizedError
        if self.require_active and user.is_active is False:
            raise DomainInactiveUserError(
                message=ErrorMessages.account_is_blocked.format(
                    str(PublicAttrNamesEnum.username), decoded_token.sub
                )
            )
        if self.require_role is not None and user.role != self.require_role:
            raise DomainUserPermissionError(
                message=ErrorMessages.has_not_access.format(
                    str(PublicAttrNamesEnum.username), decoded_token.sub
                )
            )
        return user
