from typing import Protocol


class UsersCacheProtocol(Protocol):
    async def get_by_id(self, _id: int): ...
