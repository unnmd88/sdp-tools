import logging
from dataclasses import dataclass

from app_logging.dev.config import DOMAIN


logger = logging.getLogger(DOMAIN)

#
# @dataclass(frozen=True, slots=True, kw_only=True)
# class GetUserFromRepoByJWTUseCaseImpl:
#     service: GetUserFromRepoByJWTServiceProtocol
#
#     async def __call__(self, access_token: str) -> UserDTO:
#         user_entity = await self.service(token=access_token)
#         try:
#             return UserDTO(**user_entity.to_dict())
#         except (
#             DomainEntityNotFoundError,
#             DomainUnauthorizedError,
#             DomainUserPermissionError,
#         ) as e:
#             raise UseCaseError(
#                 message=e.message,
#                 code=e.code,
#                 http_status=e.http_status,
#             )
#         except DomainError as e:
#             e.subject = self.__class__.__name__
#             e.context |= {
#                 "access_token": f"{access_token}",
#                 "user_entity": f"{user_entity}",
#             }
#             logger.error(e)
#             raise UseCaseError
