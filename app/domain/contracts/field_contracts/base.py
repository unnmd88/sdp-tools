from abc import ABC
from collections.abc import Sequence, Iterable

from types import UnionType
from typing import (
    Callable,
    Any,
)


from domain.contracts.exc import (
    ContractViolationInvariantError,
    ContractViolationFieldError,
)

from domain.contracts.interfaces.cahe_interface import CacheFieldProtocol
from domain.contracts.interfaces.require_schemas_interfaces import (
    ContractRequireSchemaProtocol,
    ContractProcessValueSchemaRequireProtocol,
)
from domain.contracts.utils import replace_self_from_attr_name, SimpleCache

type RequireTypeData = ContractRequireSchemaProtocol | Callable[..., bool]
type IsInstanceType = type | tuple[type, ...] | UnionType


class AbstractContractField(ABC):
    base_requires: Sequence[ContractRequireSchemaProtocol] | None = None

    def __init_subclass__(cls, *, cache: CacheFieldProtocol | None = None, **kwargs):
        if cls.base_requires is None:
            cls.base_requires = ()
        for i, require in enumerate(cls.base_requires):
            if not isinstance(require, ContractRequireSchemaProtocol):
                raise TypeError(
                    f"Тип аргумента {cls.base_requires!r}' должен быть "
                    f"соответствовать протоколу {ContractRequireSchemaProtocol.__name__!r}. "
                    f"Предоставленный тип: {type(require)!r}. Индекс={i}."
                )
        super().__init_subclass__(**kwargs)

    def __init__(
        self,
        *,
        field_name: str,
        nullable: bool = False,
        pipeline_preprocess_value: Iterable[ContractProcessValueSchemaRequireProtocol]
        | None = None,
        pipeline_postprocess_value: Iterable[ContractProcessValueSchemaRequireProtocol]
        | None = None,
        requires: Iterable[ContractRequireSchemaProtocol] | None = None,
        invariants: Iterable[ContractRequireSchemaProtocol] | None = None,
        env_name: str | None = None,
        use_cache: bool = True,
        override_default_cache: CacheFieldProtocol | None = None,
    ):
        self._name = field_name
        self._nullable = nullable
        self._pipeline_preprocess_value = (
            tuple(pipeline_preprocess_value)
            if pipeline_preprocess_value is not None
            else ()
        )
        self._pipeline_postprocess_value = (
            tuple(pipeline_postprocess_value)
            if pipeline_postprocess_value is not None
            else ()
        )
        self._requires = tuple(requires) if requires is not None else ()
        self._invariants = tuple(invariants) if invariants is not None else ()
        self._env_name = env_name
        self._use_cache = use_cache

        self._cache = SimpleCache()
        if override_default_cache is not None:
            self.set_cache(cache=override_default_cache)

        # Проверка, что все элементы из: self._preprocess_value_requires, self._postprocess_value_require,
        # self._requires, self._invariants соответствуют протоколу ContractRequireProtocol.
        self._check_requires_is_valid()

    def _check_requires_is_valid(self) -> None:
        """Проверяет, что все элементы в каждом из контейнеров с зависимостями соответствуют протоколу."""
        to_check = [
            (requires, attr_data_as_string_for_exception)
            for requires, attr_data_as_string_for_exception in [
                (
                    self._pipeline_preprocess_value,
                    f"{self._pipeline_preprocess_value=}",
                ),
                (
                    self._pipeline_postprocess_value,
                    f"{self._pipeline_postprocess_value=}",
                ),
                (self._requires, f"{self._requires=}"),
                (self._invariants, f"{self._invariants=}"),
            ]
        ]
        for requires, name in to_check:
            for i, require in enumerate(requires):
                if not isinstance(require, ContractRequireSchemaProtocol):
                    formatted_attr_name = replace_self_from_attr_name(name)
                    raise TypeError(
                        f"Тип аргумента {formatted_attr_name!r} должен "
                        f"соответствовать протоколу {ContractRequireSchemaProtocol.__name__!r}. "
                        f"Предоставленный тип: {type(require)!r}. "
                        f"Значение={require!r}. "
                        f"Индекс={i}."
                    )

    def _validate(self, value: Any) -> Any:
        for require in self._requires:
            if not require(value):
                if require.custom_exception is not None:
                    raise require.custom_exception
                raise ContractViolationFieldError(
                    field_name=self._name,
                    contract=require.contract,
                    violation=require.violation,
                    value=value,
                    detail=require.detail,
                )
        return value

    def _check_invariants(self, value: Any) -> Any:
        for require in self._invariants:
            if not require(value):
                raise ContractViolationInvariantError(
                    field_name=self._name,
                    contract=require.contract,
                    violation=require.violation,
                    value=value,
                    detail=require.detail,
                )

    def _pipeline(
        self, *, value: Any, handlers: Sequence[ContractRequireSchemaProtocol]
    ) -> Any:
        for require in handlers:
            value = require(value)
        return value

    def __call__(self, value: Any) -> Any:
        if value is None:
            if self._nullable:
                self._check_invariants(value)
                return None
            raise ContractViolationFieldError(
                field_name=self._name,
                contract=f"'nullable'={self._nullable!r}",
                violation=f"Значение поля не может быть {None!r}",
                value=value,
            )
        if self._use_cache and (value in self._cache):
            return value
        value = self._pipeline(value=value, handlers=self._pipeline_preprocess_value)
        self._validate(value)
        value = self._pipeline(value=value, handlers=self._pipeline_postprocess_value)
        self._check_invariants(value)
        if self._use_cache:
            self._cache.add(value)
            assert value in self._cache, "Элемент не был добавлен в кеш."
        return value

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(field_name={self._name!r})"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.repr_schema()})"

    def repr_schema(self):
        return (
            f"{self.__class__.__name__}("
            f"field_name={self._name!r} "
            f"nullable={self._nullable!r} "
            f"use_cache={self._use_cache!r} "
            f"has_preprocess_value_require={bool(self._pipeline_preprocess_value)!r} "
            f"count_requires={len(self._requires)!r} "
            f"count_invariants={len(self._invariants)!r}"
            f")"
        )

    def set_cache(self, cache: CacheFieldProtocol = SimpleCache()):
        if isinstance(cache, CacheFieldProtocol):
            raise TypeError(
                f"Тип устанавливаемого кэша должен "
                f"соответствовать протоколу {CacheFieldProtocol.__name__!r}. "
                f"Предоставленный тип: {type(cache)!r}."
            )
        self._cache = cache
        assert self._cache is not None, f"Кэш не установлен cache: {self._cache!r}."

    def get_cache(self) -> CacheFieldProtocol | None:
        return self._cache

    def enable_cache(self):
        self._use_cache = True

    def disable_cache(self):
        self._use_cache = False

    @property
    def name(self):
        return self._name
