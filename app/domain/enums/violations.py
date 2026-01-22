from enum import StrEnum


class Violations(StrEnum):
    value_length = "value_length"
    invalid_type = "invalid_type"
    must_be_positive_integer = "must_be_positive_integer"
    string_must_be_alpha = "string_must_be_alpha"
    string_cant_be_numeric = "string_cant_be_numeric"
    string_cant_start_with_numeric = "string_cant_start_with_numeric"

    invariant_violation = "invariant_violation"
