from enum import StrEnum


class Violations(StrEnum):
    value_length = "value_length"
    invalid_type = "invalid_type"
    invalid_ = "invalid_type"
    does_not_match_regexp = "does_not_match_regexp"
    cannot_be_empty = "cannot_be_empty"
    must_be_positive_integer = "must_be_positive_integer"
    string_must_be_alpha = "string_must_be_alpha"
    string_cant_be_numeric = "string_cant_be_numeric"
    string_cant_start_with_numeric = "string_cant_start_with_numeric"
    invalid_enum_value = "invalid_enum_value"
    invalid_email = "invalid_email"

    invariant_violation = "invariant_violation"
