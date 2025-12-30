from dataclasses import dataclass


@dataclass(slots=True, frozen=True, kw_only=True)
class FiltersForSearchDTO:
    """ DTO для поиска сущности в хранилище. """

    search_filters: dict


@dataclass(slots=True, frozen=True, kw_only=True)
class CreateRecordDTO:
    """ DTO для создания новой записи в хранилище. """

    fields: dict


@dataclass(slots=True, frozen=True, kw_only=True)
class UpdateRecordDTO:
    """ DTO для обновления существующей записи в хранилище. """

    search_filters: dict
    fields: dict


@dataclass(slots=True, frozen=True, kw_only=True)
class DeleteRecordDTO(FiltersForSearchDTO):
    """ DTO для удаления существующей записи в хранилище. """

