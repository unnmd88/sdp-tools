from typing import Callable, Sequence, Any

from domain.contract2.require import Require
from domain.exceptions.contract_violation_exc import (
    DomainContractViolationError,
    DomainValidationError,
)


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
        self._requires = tuple(requires or ())
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
                raise DomainValidationError(
                    field_name=self._field_name,
                    subject=f"{instance.__class__.__name__}",
                    value=value,
                    contract_code="nullable",
                    violation="nullable is not allowed",
                    message=f"Значение {self._field_name!r} не может быть пустым",
                )
            value = self._preprocess(value)
            for require in self._requires:
                if not require.handler(value):
                    raise DomainContractViolationError(
                        subject=f"{instance.__class__.__name__}",
                        field_name=self._field_name,
                        handler=f"{require.handler.__name__}",
                        value=value,
                        contract_code=require.contract,
                        violation=require.violation,
                        message=require.message,
                    )
        except DomainContractViolationError as e:
            e.subject = f"{instance.__class__.__name__}"
            raise e
        if self._use_cache:
            self._cache.add(value)
            assert value in self._cache
        return setattr(instance, self.name, self._postprocess(value))

    def get_cache(self) -> set:
        return self._cache

    def clear_cache(self):
        self._cache.clear()
