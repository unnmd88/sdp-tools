from dataclasses import dataclass

from application.exceptions import ApplicationLayerError
from domain.entities import UserEntity
from domain.exceptions import DomainContractViolationError, DomainEntityNotFoundError
from domain.repositories.users_repo_interface import UsersRepositoryProtocol
from infrastructure.exceptions import InfrastructureError


@dataclass(frozen=True, slots=True, kw_only=True)
class UserServiceImpl:

    user_repository: UsersRepositoryProtocol

    async def get_user_by_username(self, username: str) -> UserEntity:
        try:
            return await self.user_repository.get_by_username(username)
        except DomainContractViolationError:
            raise DomainEntityNotFoundError
        except InfrastructureError:
            raise ApplicationLayerError
