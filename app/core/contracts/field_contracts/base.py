import itertools
from collections.abc import MutableSequence, Sequence
from datetime import timedelta, datetime
from enum import IntEnum
from time import perf_counter
from types import UnionType
from typing import (
    Callable,
    Any,
    Iterable,
    MutableMapping,
)

from core.contracts import ContractRequire
from core.exceptions.contract import (
    ContractViolationValueTypeError,
    ContractViolationPreConditionError,
    ContractViolationPreProcessingError,
)
from core.contracts.validators.domain_validators import (
    id_validator,
    isinstance_validator,
)


class ValidationLevels(IntEnum):
    strict = 60
    soft = 50
    liberal = 40


class CacheSetup:
    def __init__(
        self,
        *,
        use_cache: bool = False,
        cache: dict = None,
        expiration_time: timedelta = None,
    ):
        self._cache = cache
        if use_cache and cache is None:
            self._cache = {}
        if expiration_time is not None and not isinstance(expiration_time, timedelta):
            raise TypeError('Время жизни должно быть экземпляром класса timedelta.')
        self.expiration_time = expiration_time

    def set_cache(self, cache: MutableMapping[Any, timedelta | None]):
        if not isinstance(cache, MutableMapping):
            raise TypeError(
                f'Cache должен быть экземпляром класса {MutableMapping.__name__!r}.'
            )
        self._cache = cache

    def get_cache(self):
        return self._cache

    def get(self, value: Any):
        return self._cache.get(value)

    def update(self, **kwargs):
        self._cache.update(**kwargs)

    def pop(self, key: Any) -> Any | None:
        return self._cache.pop(key, None)

    def clear(self):
        self._cache.clear()


class ContractField[T]:
    _name_by_default: str = 'Generic'
    _expected_types: type | tuple[type, ...] | UnionType = Any
    _cache_valid_values: set[T] = set()
    _nullable_by_default: bool = False
    _requires: Sequence[ContractRequire] = ()

    __slots__ = (
        '_name',
        '_raise_if_isinstance_failed',
        '_use_cache',
        '_nullable',
        '_preprocess_value_before_requires',
        '_isinstance_check_types',
        '_all_requires',
        '_repair',
        '_level',
    )

    def __init__(
        self,
        *,
        use_cache: bool,
        name: str = None,
        nullable: bool = None,
        isinstance_check_types: bool = True,
        raise_if_isinstance_failed: bool = True,
        preprocess_value_before_requires: Callable[[T], Any | T] = None,
        extra_requires: Iterable[ContractRequire] = (),
        repair: Callable[[T], Any | T] = None,
        level: ValidationLevels = ValidationLevels.strict,
    ):
        self._name = name or self._name_by_default
        self._isinstance_check_types = isinstance_check_types
        self._use_cache = use_cache
        self._nullable = nullable or self._nullable_by_default
        self._preprocess_value_before_requires = preprocess_value_before_requires
        self._raise_if_isinstance_failed = raise_if_isinstance_failed
        if any(
            not isinstance(predicate, ContractRequire) for predicate in extra_requires
        ):
            raise TypeError(
                f'Дополнительные валидаторы должны быть итерируемым объектом, '
                f'содержащим элементы типа {ContractRequire.__name__!r}'
            )
        self._all_requires = set(
            r for r in itertools.chain(self._requires, (extra_requires or ()))
        )
        self._all_requires = tuple(self._all_requires)

        self._repair = repair
        self._level = level

        if self._preprocess_value_before_requires is not None:
            if not callable(self._preprocess_value_before_requires):
                raise TypeError(
                    'preprocess_value_before_requires должен быть вызываемым объектом'
                )
        if not isinstance(self._nullable, bool):
            raise TypeError('Nullable должно быть булевым значением')

        try:
            ValidationLevels(self._level)
        except ValueError:
            raise TypeError(
                f"Неверное значение для поля 'mode'. Допустимы из класса {ValidationLevels.__name__!r}"
            )

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'name={self._name!r} '
            f'expected_types={self._expected_types!r} '
            f'nullable_by_default={self._nullable_by_default!r} '
            f'nullable={self._nullable!r} '
            f'isinstance_check_types={self._isinstance_check_types!r} '
            f'use_cache={self._use_cache!r} '
            f'all_requires_count={len(self._all_requires)!r}'
            f')'
        )

    def __call__(self, value: T) -> T:
        if self._use_cache and (value in self._cache_valid_values):
            return value
        if value is None and self._nullable:
            return None
        try:
            value = (
                self._preprocess_value_before_requires(value)
                if self._preprocess_value_before_requires
                else value
            )
        except Exception as e:
            raise ContractViolationPreProcessingError(e)

        if not self.isinstance_validator(value):
            pass  # TODO: Если self._raise_if_isinstance_failed=False, то логировать или например метрику собирать

        value = self._validation(value)
        self._cache_valid_values.add(value)
        return value

    def _validation(self, value: Any) -> bool:
        for predicate, exception in self._requires:
            if not predicate(value):
                if self._level < ValidationLevels.strict and self._repair is not None:
                    if predicate(repaired_val := self._repair(value)):
                        return repaired_val
                if isinstance(exception, type) and issubclass(
                    exception, ContractViolationValueTypeError
                ):
                    raise ContractViolationValueTypeError(
                        arg_name=self._name,
                        got=value,
                        expected=self._expected_types,
                    )
                raise ContractViolationPreConditionError
        return value

    def isinstance_validator(self, value: Any) -> bool:
        return isinstance_validator(
            name=f'поля {self._name!r}',
            value=value,
            expected=self._expected_types,
            raise_if_failed=self._raise_if_isinstance_failed,
        )

    @classmethod
    def get_cache(cls) -> set[T]:
        return cls._cache_valid_values

    @property
    def name(self):
        return self._name

    @property
    def default_err_message(self):
        return f'Нарушен контракта поля {self._name!r}.'


class ContractFieldId(ContractField):
    _name_by_default = 'id'
    _expected_types = int
    _requires = [ContractRequire(predicate=id_validator)]

    __slots__ = ContractField.__slots__


class ContractFieldCreatedAt(ContractField):
    _name_by_default = 'created_at'
    _expected_types = datetime
    _nullable_by_default = True

    __slots__ = ContractField.__slots__


class ContractFieldUpdatedAt(ContractField):
    _name_by_default = 'updated_at'
    _expected_types = datetime
    _nullable_by_default = True

    __slots__ = ContractField.__slots__


#
#
# created_at_field_contract = FieldValidatorContract(
#     name='created_at',
#     nullable=True,
#     preconditions=[
#         ContractRequire(
#             predicate=lambda x: isinstance(x, datetime),
#             exception=ContractViolationValueTypeError,
#         ),
#     ],
# )
#
#
# updated_at_field_contract = FieldValidatorContract(
#     name='updated_at',
#     nullable=True,
#     message_expected_type_if_type_not_valid="'datetime'",
#     preconditions=[
#         ContractRequire(
#             predicate=lambda x: isinstance(x, datetime),
#             exception=ContractViolationValueTypeError,
#         ),
#     ],
# )


if __name__ == '__main__':
    # print(id_field_contract)

    id_contract = ContractFieldId(
        nullable=False,
        use_cache=True,
        extra_requires=[ContractRequire(predicate=id_validator)],
        isinstance_check_types=True,
    )
    print(id_contract._expected_types)
    print(id_contract.get_cache())
    id_contract(1)
    print(id_contract.get_cache())
    id_contract(1)
    print(id_contract.get_cache())
    id_contract(2)

    print(id_contract.get_cache())
    print(id_contract)
