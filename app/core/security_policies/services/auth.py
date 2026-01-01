from application.interfaces.services.authentication import AuthenticationSchemaProtocol
from application.interfaces.services.users_crud import UsersServiceProtocol
from core.security_policies.exceptions import InvalidUsernameOrPasswordError, InactiveUserError
from core.users.entities.user import UserEntity
from core.users.exceptions import UserNotFoundByUsernameError
from core.utils import validate_password


class UserAuthenticationServiceImpl:
    def __init__(self, user_service: UsersServiceProtocol):
        self.user_service = user_service

    async def authenticate(
        self,
        auth_data: AuthenticationSchemaProtocol,
    ) -> UserEntity:
        user_entity = await self.user_service.get_user_by_username_for_auth(auth_data.username)
        if user_entity is None:
            raise InvalidUsernameOrPasswordError
        password_is_valid = validate_password(
            password=auth_data.password,
            hashed_password=user_entity.password,
        )
        if not password_is_valid:
            raise InvalidUsernameOrPasswordError
        if not user_entity.is_active:
            raise InactiveUserError
        return user_entity
