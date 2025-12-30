from typing import Protocol

from core.dto.update_entity import UpdatedEntityDTO


class BaseCrudProtocol(Protocol):

    async def get_one_by_id_or_none(self, _id: int): ...

    async def get_one_or_none_by_filters(self, filters: dict): ...

    async def get_many(self, filters: dict | None = None): ...

    async def add(self, entity): ...

    async def update(self, _id: int, **fields,) -> UpdatedEntityDTO: ...

    async def update_one(self, filters: dict, **fields,) -> UpdatedEntityDTO: ...

    async def delete_one(self, _id: int): ...


class FiltersForSearchProtocol(Protocol):

    search_filters: dict

