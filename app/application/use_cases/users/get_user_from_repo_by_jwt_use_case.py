import logging
from dataclasses import dataclass

from app_logging.dev.config import AUTH_LOGGER, DOMAIN
from application.interfaces.services.get_user_from_repo_by_jwt_service_interface import (
    GetUserFromRepoByJWTServiceProtocol,
)
from application.use_cases.exceptions import UseCaseError
from domain.dto.users import UserDTO
from domain._exceptions.base import DomainError
from domain._exceptions.entity_not_found_exc import DomainEntityNotFoundError
from domain._exceptions.permissions_exc import (
    DomainUserPermissionError,
    DomainUnauthorizedError,
)

logger = logging.getLogger(DOMAIN)


@dataclass(frozen=True, slots=True, kw_only=True)
class GetUserFromRepoByJWTUseCaseImpl:
    service: GetUserFromRepoByJWTServiceProtocol

    async def __call__(self, access_token: str) -> UserDTO:
        user_entity = await self.service(token=access_token)
        try:
            return UserDTO(**user_entity.to_dict())
        except (
            DomainEntityNotFoundError,
            DomainUnauthorizedError,
            DomainUserPermissionError,
        ) as e:
            raise UseCaseError(
                message=e.message,
                code=e.code,
                http_status=e.http_status,
            )
        except DomainError as e:
            e.subject = self.__class__.__name__
            e.context |= {
                "access_token": f"{access_token}",
                "user_entity": f"{user_entity}",
            }
            logger.error(e)
            raise UseCaseError
