import random
import re
import secrets
import string
from dataclasses import dataclass, field
from typing import ClassVar

from core.error_codes import ErrorCodes
from domain.enums.attrs_names import PrivateAttrNamesEnum
from domain.enums.validation_err_messages import ErrorMessages
from domain.enums.violations import Violations
from domain.exceptions import (
    DomainError,
    DomainBusinessRuleError,
    DomainValidationError, DomainContractViolationError,
)
from domain.value_objects.contract_violation_context_vo import (
    ContractViolationContextVO,
)


@dataclass(frozen=True, slots=True, kw_only=True, repr=False)
class SetPasswordVO:

    MIN_LEN_PASSWORD: ClassVar[int] = 4
    MAX_LEN_PASSWORD: ClassVar[int] = 32
    CHARS: ClassVar[str] = string.ascii_letters + string.digits + "$#%*"
    PASSWORD_PATTERN: ClassVar[re.Pattern] = re.compile(r"^[a-zA-Z0-9$#*%]+$")

    subject: str | None = None
    password: str

    def __post_init__(self):

        if not isinstance(self.password, str):
            ctx = ContractViolationContextVO(
                subject=self.subject,
                field_name=str(PrivateAttrNamesEnum.password),
                handler=f"{self.__class__.__name__}:{self.__init__.__name__}",
                contract_code=ErrorCodes.DOMAIN_VALIDATION.code,
                violation=Violations.invalid_type,
                value=self.password,
                expected_type=str,
                message=ErrorMessages.expected_type_string.format(
                    str(PrivateAttrNamesEnum.password), type(self.password)
                ),
            )
            raise DomainValidationError(
                context=ctx,
                private_message=ctx.message,
                public_message="Некорректный тип данных. Для пароля ожидается строка.",
            )

        elif len(self.password) < self.MIN_LEN_PASSWORD or len(self.password) > self.MAX_LEN_PASSWORD or self.PASSWORD_PATTERN.match(self.password) is None:
            rule = (
                "Недопустимый пароль. "
                "Пароль должен быть не менее 4 и не более 32 символов и "
                "содержать только латинские буквы, цифры и символы $#%*"
            )
            ctx = ContractViolationContextVO(
                subject=self.subject,
                field_name=str(PrivateAttrNamesEnum.password),
                handler=f"{self.__class__.__name__}:{self.__init__.__name__}",
                contract_code=ErrorCodes.BUSINESS_RULE_VIOLATION.code,
                violation=Violations.invalid_password_to_set,
                value=self.password,
                rule=rule,
                message="Недопустимый пароль.",
            )
            raise DomainBusinessRuleError(
                context=ctx,
                private_message=ctx.message,
                public_message=ctx.rule,
            )

    @classmethod
    def from_generated_password(cls, subject: str = None) -> "SetPasswordVO":
        generated_password = "".join(
            secrets.choice(cls.CHARS) for _ in range(random.randint(cls.MIN_LEN_PASSWORD, cls.MAX_LEN_PASSWORD))
        )
        return cls(subject=subject, password=generated_password)


    def __repr__(self):
        return f"{self.__class__.__name__}(password=******)"


if __name__ == "__main__":
    try:
        p = SetPasswordVO(password="asasas121s")
    except DomainError as e:
        print(e)
        print(e.private_message)
        print(e.to_dict())
    print(SetPasswordVO.from_generated_password())
