from enum import Enum, StrEnum, IntEnum
from typing import Callable, Sequence, Any

from core.error_codes import ErrorCodes
from domain.contract2.require import Require
from domain.enums.validation_err_messages import ErrorMessages
from domain.enums.violations import Violations
from domain.exceptions import DomainContractViolationError, DomainValidationError
from domain.value_objects.contract_violation_context_vo import (
    ContractViolationContextVO,
)


class ContractFieldEnum[T]:
    def __init__(
        self,
        *,
        enum: type[Enum],
        field_name: str,
        nullable: bool = False,
        use_cache: bool = False,
    ):
        self._enum = enum
        self._field_name = field_name
        self._nullable = nullable
        self._use_cache = use_cache
        self._cache = set()

    def __set_name__(self, owner, name):
        self.name = f"_{name}"

    def __get__(self, obj, owner=None) -> T:
        if obj is None:
            return self
        return getattr(obj, self.name)

    def __set__(self, instance, value):
        if (value is None and self._nullable) or (
            self._use_cache and value in self._cache
        ):
            return setattr(instance, self.name, self._enum(value))
        try:
            if value is None and not self._nullable:
                current_error_context = ContractViolationContextVO(
                    contract_code="nullable",
                    violation=Violations.nullable_false,
                    message=f"Значение {self._field_name!r} не может быть None",
                    handler="check_nullable",
                )
                raise DomainValidationError(
                    private_message=current_error_context.message,
                    public_message=f"Значение не должно быть пустым.",
                    context=current_error_context,
                )

            try:
                value = self._enum(value)
            except ValueError:
                if self._enum == StrEnum:
                    expected_type = str
                elif self._enum == IntEnum:
                    expected_type = int
                else:
                    expected_type = self._enum
                ctx = ContractViolationContextVO(
                    handler=self.__class__.__name__,
                    contract_code=ErrorCodes.DOMAIN_VALIDATION.code,
                    violation=Violations.invalid_enum_value,
                    value=value,
                    expected_type=expected_type,
                    message=ErrorMessages.invalid_enum_value.format(
                        self.__class__.__name__, value
                    ),
                )
                raise DomainValidationError(
                    context=ctx,
                    public_message=ErrorMessages.must_be_member_of_enum.format(
                        self._field_name, list(self._enum)
                    ),
                )
        except DomainContractViolationError as e:
            cur_ctx = e.context or ContractViolationContextVO()
            updated_context = ContractViolationContextVO(
                subject=cur_ctx.subject or f"{instance.__class__.__name__}",
                field_name=cur_ctx.field_name or self._field_name,
                contract_code=cur_ctx.contract_code,
                violation=cur_ctx.violation,
                handler=cur_ctx.handler,
                message=cur_ctx.message,
                value=cur_ctx.value or value,
            )
            e.update_context(updated_context)
            raise e
        if self._use_cache:
            self._cache.add(value)
            assert value in self._cache
        return setattr(instance, self.name, value)

    def get_cache(self) -> set:
        return self._cache

    def clear_cache(self):
        self._cache.clear()

