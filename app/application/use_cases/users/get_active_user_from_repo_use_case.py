import logging
from dataclasses import dataclass

from app_logging.dev.config import DOMAIN
from application.dto.users import UserDTO
from application.exceptions import InactiveAccountError
from domain.exceptions import DomainEntityNotFoundError
from domain.repositories.users_repo_interface import UsersRepositoryProtocol

logger = logging.getLogger(DOMAIN)


@dataclass(frozen=True, slots=True, kw_only=True)
class GetActiveUserFromRepoUseCase:
    user_repository: UsersRepositoryProtocol

    async def __call__(self, _id: int) -> UserDTO:
        user = await self.user_repository.get_by_id(_id)
        if user is None:
            raise DomainEntityNotFoundError(
                private_message=f"Пользователь c id={_id} не найден.",
                public_message="Пользователь не найден.",
            )
        if not user.is_active:
            raise InactiveAccountError(
                private_message=f"Аккаунт пользователя с id={_id} не активен.",
                public_message="Аккаунт не активен. Пожалуйста, свяжитесь с администратором.",
            )
        return UserDTO.from_entity(user)
