from typing import Protocol

from domain.dto.common import (
    UpdatedRecordDTO,
    CreateRecordDTO,
    ToUpdateRecordDTO,
    FiltersForSearchDTO,
)


class BaseCrudProtocol(Protocol):
    async def get_one_by_id_or_none(self, _id: int): ...

    async def get_one_or_none_by_filters(self, filters: dict): ...

    async def get_many(self, filters: dict | None = None): ...

    async def add(self, create_record_dto: CreateRecordDTO): ...

    # async def update(self, _id: int, **fields,) -> UpdatedRecordDTO: ...

    async def update_one(
        self, update_record_dto: ToUpdateRecordDTO
    ) -> UpdatedRecordDTO: ...

    async def delete_one(self, filters: FiltersForSearchDTO): ...


class FiltersForSearchProtocol(Protocol):
    search_filters: dict
