from dataclasses import dataclass

from core.error_codes import ErrorCodes
from domain.enums.attrs_names import PrivateAttrNamesEnum
from domain.enums.validation_err_messages import ErrorMessages
from domain.enums.violations import Violations
from domain.exceptions import DomainValidationError
from domain.value_objects.contract_violation_context_vo import ContractViolationContextVO


@dataclass(frozen=True, slots=True, kw_only=True, repr=False)
class PasswordVO:

    password: bytes
    subject: str

    def __post_init__(self):
        if self.password and isinstance(self.password, bytes):
            return
        private_message = ErrorMessages.expected_hashed_password.format(
            str(PrivateAttrNamesEnum.password)
        )
        public_message = private_message
        ctx = ContractViolationContextVO(
            subject=self.subject,
            field_name=str(PrivateAttrNamesEnum.password),
            handler=f"{self.__class__.__name__}: {self.__post_init__.__name__}",
            contract_code=ErrorCodes.DOMAIN_VALIDATION.code,
            violation=Violations.invalid_type,
            value=self.password,
            message=private_message,
        )
        raise DomainValidationError(
            context=ctx,
            private_message=private_message,
            public_message=public_message,
        )

    def __repr__(self):
        return f"{self.__class__.__name__}(password=******)"


if __name__ == "__main__":
    p = PasswordVO("1231")
    print(p)
