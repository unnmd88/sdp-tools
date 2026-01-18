import re
from typing import Pattern


def replace_self_from_attr_name(attr: str) -> str:
    new_name = attr.split("=")[0].replace("self.", "")
    return new_name[1:] if new_name.startswith("_") else new_name


def validate_string_by_pattern(
    *,
    target: str,
    pattern: Pattern | str,
) -> bool:
    return (pattern is None) or (re.match(pattern, target) is not None)


class SimpleCache:
    def __init__(self):
        self._cache = set()

    def __repr__(self):
        return f"{self.__class__.__name__}({self._cache!r})"

    def __len__(self):
        return len(self._cache)

    def __contains__(self, value):
        return value in self._cache

    def add(self, value):
        self._cache.add(value)

    def clear(self):
        self._cache.clear()


if __name__ == "__main__":
    s = re.compile("[a-z]+")
