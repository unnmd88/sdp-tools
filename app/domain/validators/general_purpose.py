from core.error_codes import ErrorCodes
from domain.enums.attrs_names import PublicAttrNamesEnum
from domain.enums.validation_err_messages import ErrorMessages
from domain.enums.violations import Violations
from domain.exceptions import DomainError, DomainValidationError
from domain.value_objects.contract_violation_context_vo import (
    ContractViolationContextVO,
)


class GeneralPurposeValidator:
    @classmethod
    def pk_id(
        cls,
        value: str,
        subject: str | None = None,
    ) -> bool:
        if isinstance(value, int) and value > 0 and value:
            return True
        field_name = str(PublicAttrNamesEnum.id)
        if not isinstance(value, int):
            violation = Violations.invalid_type
        elif value < 1:
            violation = Violations.must_be_positive_integer
        else:
            raise DomainError
        if isinstance(value, str) and value.isdigit():
            value = f"{value}(Строка)"
        context = ContractViolationContextVO(
            field_name=field_name,
            subject=subject,
            handler=f"{cls.__name__!r}:{cls.pk_id.__name__!r}",
            contract_code=ErrorCodes.DOMAIN_TYPE_VALIDATION.code,
            violation=violation,
            value=value,
            expected_type=int.__name__,
            message=ErrorMessages.expected_type_positive_int.format(field_name, value),
        )
        raise DomainValidationError(
            message=context.message,
            context=context,
        )
