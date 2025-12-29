from dataclasses import dataclass, field

from core.enums import RegionCodes, RegionNames


@dataclass(slots=True, frozen=True, kw_only=True)
class RegionDTO:
    """ DTO для экземпляра существующего региона. """
    code: int
    name: str


# @dataclass(slots=True, frozen=True, kw_only=True)
# class RegionFiltersForSearchDTO:
#     """ DTO для экземпляра существующего региона. """
#     # code: int | None = None
#     # name: str | None = None
#     filters_for_search: dict = field(default_factory=dict)
#
#
#     @classmethod
#     def get_dto_instance(cls, code_or_name: str | int):
#         code = int(code_or_name) if code_or_name.isdigit() else None
#         name = None if code else code_or_name
#         return RegionFiltersForSearchDTO(code=code, name=name,)


@dataclass(slots=True, frozen=True, kw_only=True)
class UpdateRegionDTO:
    """ DTO для обновления существующего региона. """
    # region_name_to_update: RegionNames
    filters_for_search: dict
    code_or_name: str

    code: int | None = None
    name: str | None = None


@dataclass(slots=True, frozen=True, kw_only=True)
class CreateRegionDTO(RegionDTO):
    """ DTO для создания нового региона. """


