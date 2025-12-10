from typing import Any
from core.users.entities.user import UserEntity
from core.users.exceptions import UserInactiveError


class BaseService:

    def __init__(
        self,
        user_entity: UserEntity,
        repository: Any
    ):

        self.user_entity = user_entity
        self.repository = repository
        if not user_entity.is_active:
            raise UserInactiveError