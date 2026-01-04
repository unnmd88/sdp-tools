from typing import Any
from core.users.entities.user import UserEntity
from core.users.exceptions import UserInactiveError


class BaseService:

    def __init__(
        self,
        user_entity: UserEntity,
        repository: Any,
        raise_if_user_inactive: bool = True,
    ):

        self.user_entity = user_entity
        if not isinstance(self.user_entity, UserEntity):
            raise AttributeError
        if raise_if_user_inactive and not user_entity.is_active:
            raise UserInactiveError
        self.repository = repository

