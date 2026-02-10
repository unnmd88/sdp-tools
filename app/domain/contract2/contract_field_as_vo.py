from typing import Callable, Sequence, Any, Protocol, runtime_checkable

from domain.contract2.require import Require
from domain.enums.violations import Violations
from domain.exceptions import DomainContractViolationError, DomainValidationError
from domain.value_objects.contract_violation_context_vo import (
    ContractViolationContextVO,
)

@runtime_checkable
class CacheProtocol(Protocol):
    def __getitem__(self, key: Any) -> Any: ...
    def __setitem__(self, key: Any, value: Any) -> None: ...
    def __contains__(self, key: Any) -> bool: ...
    def get(self, key: Any, default: Any = None) -> Any: ...


class ContractFieldAsVO[T_ValueObject]:
    def __init__(
        self,
        *normalizers: Callable[[str], str],
        value_object: type[T_ValueObject],
        field_name: str,
        nullable: bool = False,
        preprocess_value: Callable[[Any], Any] = None,
        use_cache=False,
        custom_cache: CacheProtocol = None,
    ):
        for i, normalizer in enumerate(normalizers):
            if not callable(normalizer):
                raise TypeError(f"Все нормализаторы должны быть "
                                f"вызываемыми объектами. Невалидный: {normalizer!r}, pos: {i}")
        self._normalizers = tuple(normalizers)
        self._value_object = value_object
        self._field_name = field_name
        self._nullable = nullable
        self._preprocess = preprocess_value or (lambda x: x) # Identity по умолчанию
        self._use_cache = use_cache
        if custom_cache is not None:
            if not isinstance(custom_cache, CacheProtocol):
                raise TypeError(f"cache_factory должен соответствовать протоколу {CacheProtocol.__name__}")
            self._cache = custom_cache
        else:
            self._cache = dict()

    def __set_name__(self, owner, name):
        self.name = f"_{name}"

    def __get__(self, obj, owner=None):
        if obj is None:
            return self
        return getattr(obj, self.name)

    def __set__(self, instance, value):
        if value is None:
            if self._nullable:
                return setattr(instance, self.name, value)
            else:
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
        if self._use_cache and (vo_from_cache := self._cache.get(value)) is not None:
            return setattr(instance, self.name, vo_from_cache)


        if (value is None and self._nullable) or (
                self._use_cache and value in self._cache
        ):
            return setattr(instance, self.name, value)
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
            value = self._preprocess(value)
            for require in self._requires:
                if not require.handler(value):
                    current_error_context = ContractViolationContextVO(
                        handler=f"{require.handler.__name__}",
                        contract_code=require.contract,
                        violation=require.violation,
                        message=require._private_message,
                    )
                    raise DomainContractViolationError(
                        private_message=current_error_context.message,
                        public_message=f"Ошибка валидации. Проверьте корректность значения поля {self._field_name!r}",
                        context=current_error_context,
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
        return setattr(instance, self.name, self._postprocess(value))

    def get_cache(self) -> set:
        return self._cache

    def clear_cache(self):
        self._cache.clear()