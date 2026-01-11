# from core.dto.filters import FiltersForSearchDTO
from core.dto.common import FiltersForSearchDTO


def get_filters_for_region_or_name_search(
    code_or_name: str | int,
) -> FiltersForSearchDTO:
    filters = {}
    if isinstance(code_or_name, int) or code_or_name.isdigit():
        filters['code'] = int(code_or_name)
    else:
        filters['name'] = code_or_name
    return FiltersForSearchDTO(filters_for_search=filters)
