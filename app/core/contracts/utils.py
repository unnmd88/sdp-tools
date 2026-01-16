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


if __name__ == "__main__":
    s = re.compile("[a-z]+")
