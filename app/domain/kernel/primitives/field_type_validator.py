from dataclasses import dataclass
from types import UnionType

from core.error_codes import ErrorCodes
from domain.kernel.enums.validation_err_messages import ErrorMessages
from domain.kernel.enums.violations import Violations
from domain.exceptions import DomainValidationError
from domain.value_objects.contract_violation_context_vo import ContractViolationContextVO


@dataclass(slots=True, kw_only=True, frozen=True)
class FieldTypeValidator[T]:

    value: T
    expected_type: type | tuple[type, ...] | UnionType
    field_name: str
    exception: type[DomainValidationError] = DomainValidationError

    def validate(self) -> T:
        if not isinstance(self.value, self.expected_type):
            private_message = ErrorMessages.invalid_type.format(self.field_name, self.value, self.expected_type)
            public_message = ErrorMessages.invalid_field_format.format(self.value)
            contract_code = ErrorCodes.DOMAIN_VALIDATION.code
            violation = Violations.invalid_type
            context = ContractViolationContextVO(
                handler=f"{self.__class__.__name__!r}:{self.validate.__name__!r}",
                contract_code=contract_code,
                violation=violation,
                value=self.value,
                expected_type=self.expected_type,
                message=private_message,
            )
            raise self.exception(
                private_message=private_message, public_message=public_message, context=context
            )
        return self.value


if __name__ == '__main__':
    v = FieldTypeValidator(
        value="1", expected_type=str, field_name='test'
    ).validate()
    print(v)