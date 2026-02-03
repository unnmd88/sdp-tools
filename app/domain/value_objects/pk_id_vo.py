from dataclasses import dataclass

from core.error_codes import ErrorCodes
from domain.enums.attrs_names import PublicAttrNamesEnum
from domain.enums.validation_err_messages import ErrorMessages
from domain.enums.violations import Violations
from domain.exceptions import DomainError
from domain.value_objects.contract_violation_context_vo import ContractViolationContextVO
from infrastructure.exceptions import RepositoryCorruptedError


@dataclass(frozen=True, slots=True, kw_only=True)
class PkIdVO:
    subject: type
    value: int

    def post_init(self):
        if isinstance(self.value, int) and self.value > 0:
            return True
        field_name = str(PublicAttrNamesEnum.id)
        if not isinstance(self.value, int):
            violation = Violations.corrupted_data_in_repository
            private_message = ErrorMessages.id_must_be_int.format(type(self.value))
        elif self.value < 1:
            violation = Violations.corrupted_data_in_repository
            private_message = ErrorMessages.id_range
        else:
            raise DomainError
        if isinstance(self.value, str) and self.value.isdigit():
            value = f"{self.value}(Строка)"
        context = ContractViolationContextVO(
            field_name=field_name,
            subject=self.subject,
            handler=f"{self.__class__.__name__!r}:{self.post_init.__name__!r}",
            contract_code=ErrorCodes.REPOSITORY_CORRUPTED_ERROR.code,
            violation=violation,
            value=value,
            expected_type=int.__name__,
            message=private_message,
        )
        raise RepositoryCorruptedError(
            private_message=context.message,
            context=context,
        )