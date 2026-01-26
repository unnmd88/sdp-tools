from domain._exceptions.contract_violation_exc import DomainValidationError


class TypeCheckerMixin:
    mapping = {
        str: "строкового",
        int: "целочисленного",
        bool: "логического",
        float: "вещественного",
    }

    @classmethod
    def check_isinstance(cls, *, field_name, value, expected_type):
        if not isinstance(value, expected_type):
            raise DomainValidationError()
