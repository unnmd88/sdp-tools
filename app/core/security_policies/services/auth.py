from application.interfaces.services.authentication import AuthenticationSchemaProtocol
from application.interfaces.services.users_crud import UsersServiceProtocol
from auth.exceptions import InvalidUsernameOrPasswordException, InactiveUserException
from core.users.entities.user import UserEntity
from core.utils import validate_password


class UserAuthenticationServiceImpl:
    def __init__(self, user_service: UsersServiceProtocol):
        self.user_service = user_service

    async def authenticate(
        self,
        auth_data: AuthenticationSchemaProtocol,
    ) -> UserEntity:
        if (
            user_entity := await self.user_service.get_user_by_username_or_none(
                auth_data.username
            )
        ) is None:
            raise InvalidUsernameOrPasswordException
        password_is_valid = validate_password(
            password=auth_data.password,
            hashed_password=user_entity.password,
        )
        if not password_is_valid:
            raise InvalidUsernameOrPasswordException
        if not user_entity.is_active:
            raise InactiveUserException(user_entity.username)
        return user_entity
