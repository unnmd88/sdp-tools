from application.interfaces.repositories.users import UsersRepositoryProtocol
from application.interfaces.services.users import UsersServiceProtocol
from application.jwt_utils import ManagerJWT
from core.dto.auth import UserAuthDTO
from core.users.exceptions import UserNotFoundByIdError


class AuthAndJWTUseCaseImpl:

    def __init__(
        self,
        user_service: UsersServiceProtocol
    ):
        self.user_service = user_service

    async def authenticate_and_issue_jwt(
        self,
        auth_data: UserAuthDTO,
        refresh_token: bool,
    ):
        user_entity = await self.user_service.authenticate(auth_data) # InvalidUsernameOrPasswordError если логин/пароль неверный.
        return ManagerJWT.issue_jwt(
            user_entity=user_entity,
            refresh_token=refresh_token,
        )

    async def issue_jwt_by_user_id(
        self,
        user_id: int,
        refresh_token: bool,
    ):
        user_entity = await self.user_service.repository.get_one_by_id_or_none(user_id)
        if user_entity is None:
            raise UserNotFoundByIdError
        return ManagerJWT.issue_jwt(
            user_entity=user_entity,
            refresh_token=refresh_token,
        )


