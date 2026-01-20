from enum import StrEnum

from domain.users.business_rules import MIN_LEN_USERNAME, MAX_LEN_USERNAME


class BusinessRulePatterns(StrEnum):
    value_str_length_range = "Значение должно быть в диапазоне от {} до {} символов"

    username_length_range = value_str_length_range.format(
        MIN_LEN_USERNAME, MAX_LEN_USERNAME
    )
