from core.dto.filters import FiltersForSearchDTO


def get_filters_for_region_or_name_search(code_or_name: str) -> FiltersForSearchDTO:
    filters = {}
    if code_or_name.isdigit():
        filters['code'] = int(code_or_name)
    else:
        filters['name'] = code_or_name
    return FiltersForSearchDTO(filters_for_search=filters)
