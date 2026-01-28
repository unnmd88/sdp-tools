from typing import Callable, Sequence, Any

from domain.contract2.require import Require
from domain.exceptions import DomainContractViolationError, DomainValidationError
from domain.value_objects.contract_violation_context_vo import ContractViolationContextVO


class ContractField:
    def __init__(
        self,
        *,
        field_name: str,
        nullable=False,
        preprocess_value: Callable[[Any], Any] = None,
        requires: Sequence[Require | Callable[[Any], bool]] = None,
        postprocess_value: Callable[[Any], Any] = None,
        use_cache=False,
    ):
        self._field_name = field_name
        self._nullable = nullable
        self._preprocess = (
            preprocess_value if preprocess_value is not None else lambda x: x
        )  # Identity по умолчанию
        # self._requires = tuple(requires or ())
        self._requires = []
        for r in requires or ():
            if isinstance(r, Require):
                pass
            elif callable(r):
                self._requires.append(Require(handler=r))
            else:
                raise TypeError("requires должен быть Require или callable")
        self._requires = tuple(self._requires)
        self._postprocess = (
            postprocess_value if postprocess_value is not None else lambda x: x
        )  # Identity по умолчанию
        self._use_cache = use_cache
        self._cache = set()

    def __set_name__(self, owner, name):
        self.name = f"_{name}"

    def __get__(self, obj, owner=None):
        if obj is None:
            return self
        return getattr(obj, self.name)

    def __set__(self, instance, value):
        if (value is None and self._nullable) or (
            self._use_cache and value in self._cache
        ):
            return setattr(instance, self.name, value)
        try:
            if value is None and not self._nullable:
                current_error_context = ContractViolationContextVO(
                    contract_code="nullable",
                    violation="Значение не может быть None",
                    message=f"Значение {self._field_name!r} не может быть пустым",
                    handler="check_nullable",
                )
                raise DomainValidationError(
                    message=current_error_context.message,
                    context=current_error_context
                )
            value = self._preprocess(value)
            for require in self._requires:
                if not require.handler(value):
                    current_error_context = ContractViolationContextVO(
                        handler=f"{require.handler.__name__}",
                        contract_code=require.contract,
                        violation=require.violation,
                        message=require.message,
                    )
                    raise DomainContractViolationError(
                        message=current_error_context.message,
                        context=current_error_context
                    )
        except DomainContractViolationError as e:
            cur_ctx: ContractViolationContextVO = e.context or ContractViolationContextVO()
            updated_context = ContractViolationContextVO(
                subject=cur_ctx.subject or f"{instance.__class__.__name__}",
                field_name=cur_ctx.field_name or self._field_name,
                contract_code=cur_ctx.contract_code,
                violation=cur_ctx.violation,
                handler=cur_ctx.handler,
                message=cur_ctx.message,
                value=cur_ctx.value or value
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
