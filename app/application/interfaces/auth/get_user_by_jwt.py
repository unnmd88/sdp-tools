from typing import Protocol

from core.users.services.crud import UsersServiceImpl


class GetUserByJWT(Protocol):
    def __init__(self, user: UsersServiceImpl): ...
