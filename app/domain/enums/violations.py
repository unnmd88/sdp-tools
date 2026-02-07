from enum import StrEnum


class Violations(StrEnum):
    corrupted_data_in_repository = "corrupted_data_in_repository"
    invalid_length = "invalid_length"
    invalid_password_to_set = "invalid_password_to_set"
    invalid_type = "invalid_type"
    does_not_match_regexp = "does_not_match_regexp"
    nullable_false = "nullable_false"
    cannot_be_empty = "cannot_be_empty"
    must_be_positive_integer = "must_be_positive_integer"
    string_must_be_alpha = "string_must_be_alpha"
    string_cant_be_numeric = "string_cant_be_numeric"
    string_cant_start_with_numeric = "string_cant_start_with_numeric"
    invalid_enum_value = "invalid_enum_value"
    invalid_email = "invalid_email"
    invalid_integer_range = "invalid_integer_range"

    invariant_violation = "invariant_violation"
