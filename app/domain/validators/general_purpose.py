from core.error_data import ErrorData
from domain.enums.public_attrs import PublicAttrsEnum
from domain.enums.validation_err_messages import ErrorMessages
from domain.enums.violations import Violations
from domain.exceptions.base import DomainError
from domain.exceptions.contract_violation_exc import DomainValidationError


class GeneralPurposeValidator:

    @classmethod
    def pk_id(cls, value: str) -> bool:
        if isinstance(value, int) and value > 0 and value:
            return True
        field_name = str(PublicAttrsEnum.id)
        if not isinstance(value, int):
            violation = Violations.invalid_type
        elif value < 1:
            violation = Violations.must_be_positive_integer
        else:
            raise DomainError
        raise DomainValidationError(
            field_name=field_name,
            handler=repr(cls.pk_id.__name__),
            contract_name=ErrorData.DOMAIN_VALIDATION.code,
            violation=violation,
            value=value,
            message=ErrorMessages.expected_type_positive_int.format(
                field_name, value
            ),
        )

        if not isinstance(value, int):
            message = ErrorMessages.expected_type_positive_int.format(field_name, value)
        if value < 1:
            violation = Violations.must_be_positive_integer
            message = ErrorMessages.cant_be_positive_integer.format(field_name, value)