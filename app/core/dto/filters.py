from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True, kw_only=True)
class FiltersForSearchDTO:
    """ DTO для поиска сущности в хранилище. """

    filters_for_search: dict

