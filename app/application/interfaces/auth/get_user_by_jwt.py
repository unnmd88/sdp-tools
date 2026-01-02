from typing import Protocol

from core.users.services.main_service import UsersServiceImpl


class GetUserByJWT(Protocol):
    def __init__(self, user: UsersServiceImpl): ...
