import logging
from dataclasses import dataclass

from app_logging.dev.config import DOMAIN
from application.dto.users import UserDTO
from application.exceptions import NotFoundError, InactiveAccountError
from domain.repositories.users_repo_interface import UsersRepositoryProtocol

logger = logging.getLogger(DOMAIN)


@dataclass(frozen=True, slots=True, kw_only=True)
class GetActiveUserFromRepoUseCase:

    user_repository: UsersRepositoryProtocol

    async def __call__(self, _id: int) -> UserDTO:
        user = await self.user_repository.get_by_id(_id)
        if user is None:
            raise NotFoundError(message="Пользователь не найден.")
        if not user.is_active:
            raise InactiveAccountError(message="Аккаунт не активен.")
        return UserDTO.from_entity(user)