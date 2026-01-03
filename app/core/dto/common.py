from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True, frozen=True, kw_only=True)
class FiltersForSearchDTO:
    """ DTO для поиска сущности в хранилище. """

    search_filters: dict


@dataclass(slots=True, frozen=True, kw_only=True)
class CreateRecordDTO:
    """ DTO для создания новой записи в хранилище. """

    fields: dict
    check_exists_search_filters: dict = field(default_factory=dict)


@dataclass(slots=True, frozen=True, kw_only=True)
class ToUpdateRecordDTO:
    """ DTO для обновления существующей записи в хранилище. """

    search_criteria: dict
    fields: dict


@dataclass(slots=True, frozen=True, kw_only=True)
class DeleteRecordDTO(FiltersForSearchDTO):
    """ DTO для удаления существующей записи в хранилище. """


@dataclass
class UpdatedRecordDTO:

    old: Any
    new: Any

    name: str | None = None


    # TODO
    # count_updated_fields: int
    # updated_fields: list = field(default_factory=list)

