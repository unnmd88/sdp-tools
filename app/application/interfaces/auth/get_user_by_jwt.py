from typing import Protocol

from core.users.services.get_user import UserServiceImpl


class GetUserByJWT(Protocol):
    def __init__(self, user: UserServiceImpl):
        ...