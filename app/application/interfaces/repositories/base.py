from typing import Protocol


class BaseRepositoryProtocol(Protocol):

    def get_by_id(self, _id: int): ...

    def get_by_name(self, name: str): ...