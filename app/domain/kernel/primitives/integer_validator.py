from typing import Self

from domain.kernel.enums.validation_err_messages import ErrorMessages
from domain.exceptions import DomainValidationError, DomainBusinessRuleError, DomainContractViolationError


class IntegerValidator:

    __slots__ = ("_value", )

    def __init__(self,value: int,):
        self._value = value

    @classmethod
    def validate_of(cls, value: int) -> Self:
        return cls(value=value)

    def ensure_gt(
        self,
        gt: int,
        exception: type[DomainContractViolationError] = DomainValidationError
    ) -> Self:
        if self._value > gt:
            return self
        message = ErrorMessages.must_be_gt.format(gt, self._value)
        raise exception(
            private_message=message,
            public_message=message,
        ).with_validator_if_has_not(f"{self.__class__.__name__!r}:{self.ensure_gt.__name__!r}")

    def ensure_lt(
        self,
        lt: int,
        exception: type[DomainValidationError] = DomainValidationError,
    ) -> Self:
        if self._value > lt:
            return self
        message = ErrorMessages.must_be_lt.format(lt, self._value)
        raise exception(
            private_message=message,
            public_message=message,
        ).with_validator_if_has_not(f"{self.__class__.__name__!r}:{self.ensure_lt.__name__!r}")

    def ensure_positive(
        self,
        exception: type[DomainValidationError] = DomainValidationError
    ) -> Self:
        """Минимальная длина."""
        if self._value > 0:
            return self
        message = ErrorMessages.must_be_positive.format(self._value)
        raise exception(
            private_message=message,
            public_message=message,
        ).with_validator_if_has_not(f"{self.__class__.__name__!r}:{self.ensure_positive.__name__!r}")

    def get(self) -> int:
        return self._value


if __name__ == '__main__':
    iv = (
        IntegerValidator.validate_of(10)
        .ensure_positive()
        .ensure_gt(10, DomainBusinessRuleError)
    )