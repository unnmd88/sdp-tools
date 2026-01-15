from abc import ABC
from collections.abc import Sequence
from enum import Enum

from types import UnionType
from typing import (
    Callable,
    Any,
    Union, get_args, TypeVar, )


from core.contracts.exc import (
    ContractViolationPreProcessingError,
    ContractViolationInvariantError,
    ContractViolationFieldError,
)

from core.contracts.interfaces.cahe_interface import CacheFieldProtocol
from core.contracts.interfaces.require import ContractRequireProtocol, ContractPreprocessRequireProtocol
from core.contracts.requires import ContractRequire
from core.contracts.utils import replace_self_from_attr_name

type RequireTypeData = ContractRequireProtocol | Callable[..., bool]
type IsInstanceType = type | tuple[type, ...] | UnionType


# class ContractField[T]:
#     _is_enum_cls_: bool = False
#     _cache: CacheFieldProtocol = set[T]()
#
#     expected_types: IsInstanceType = object
#     base_requires: Sequence[ContractRequireProtocol] = ()
#
#     def __init_subclass__(cls, *, cache: CacheFieldProtocol = None, **kwargs):
#         if cache is None:
#             cls._cache = set()
#         else:
#             cls._cache = cache
#         for require in cls.base_requires:
#             if not cls._check_valid_require(require):
#                 raise TypeError(
#                     f"Тип аргумента 'require' должен быть "
#                     f"{ContractRequire.__name__!r} или callable-объектом."
#                     f"Предоставленный тип: {type(require)!r}."
#                 )
#         if cls.expected_types and issubclass(cls.expected_types, Enum):
#             cls._is_enum_cls_ = True
#         cls._check_types_for_isinstance(cls.expected_types)
#         super().__init_subclass__(**kwargs)
#
#     @classmethod
#     def _check_valid_require(cls, require: RequireTypeData) -> bool:
#         return isinstance(require, ContractRequire) or callable(require)
#
#     @classmethod
#     def _check_types_for_isinstance(cls, value: Any) -> bool:
#         if isinstance(value, type):
#             return True
#         if isinstance(value, UnionType):
#             return True
#         if value and isinstance(value, Iterable) and all(isinstance(t, type) for t in value):
#             return True
#         if value and issubclass(value, Enum):
#             return True
#         raise TypeError(
#             f"Для проверки типов данных в {cls!r}.Ожидается:\n"
#             f"тип (Например: bool)\nили объединение 'UnionType'(например: int | str)"
#             f"\nили кортеж типов(например: (list, tuple, dict)). "
#             f"Получено: {value!r}({type(value)!r})."
#         )
#
#     def __init__(
#             self,
#             *,
#             name: str,
#             use_cache: bool,
#             nullable: bool = None,
#             check_isinstance: bool = True,
#             preprocess_value_before_requires: ContractRequireProtocol = None,
#             override_self_expected_types: IsInstanceType = None,
#             override_isinstance_base_validator: ContractRequireProtocol = None,
#             extra_requires: Iterable[ContractRequireProtocol] = (),
#             env_name: str = None,
#             level: ValidationLevels = ValidationLevels.strict,
#     ):
#         if self._is_enum_cls_ is None:
#             self._current_isinstance_validator = self._isinstance_validator
#         else:
#             self._current_isinstance_validator = self._isinstance_enum_validator
#         self._name = name
#         self._check_isinstance = check_isinstance
#         self._nullable = nullable
#         self._use_cache = use_cache
#         self._override_self_expected_types = override_self_expected_types
#         self._override_isinstance_base_validator = override_isinstance_base_validator
#         self._check_override_isinstance_base_validator()
#
#         self._env_name = env_name
#
#         if override_self_expected_types is not None:
#             self._check_types_for_isinstance(override_self_expected_types)
#             self._expected_types = override_self_expected_types
#         else:
#             self._expected_types = self.expected_types
#
#         self._is_enum = issubclass(self._expected_types, Enum)
#         if self._is_enum:
#             self._current_isinstance_validator = self._isinstance_enum_validator
#
#         self._preprocess_value_before_requires = preprocess_value_before_requires
#         # Проверка preprocess_value_before_requires
#         self._extra_requires = extra_requires
#         self._all_requires = tuple(self._collect_requires_pipeline())
#         # Финальная проверка, что все элементы в _all_requires - ContractRequire
#         for i, require in enumerate(self._all_requires):
#             assert isinstance(require, ContractRequire), (
#                 f"Все элементы в {self._all_requires!r} "
#                 f"должны быть экземплярами класса {ContractRequire.__name__!r}."
#                 f"Недопустимый объект: {require!r}  c индексом={i}."
#             )
#         self._level = level
#
#         if not isinstance(self._nullable, bool):
#             raise TypeError("аргумент 'nullable' должен быть булевым значением")
#         try:
#             ValidationLevels(self._level)
#         except ValueError:
#             raise TypeError(
#                 f"Неверное значение атрибута 'mode'. Допустимы из класса {ValidationLevels.__name__!r}"
#             )
#
#     def _check_override_isinstance_base_validator(self) -> bool:
#         if self._override_isinstance_base_validator is None:
#             return True
#         if self._override_isinstance_base_validator:
#             if isinstance(self._override_isinstance_base_validator, ContractRequire):
#                 return True
#             if callable(self._override_isinstance_base_validator):
#                 return True
#         raise TypeError(
#             f"Аргумент 'override_isinstance_base_validator' должен быть "
#             f"экземпляром класса {ContractRequire.__name__!r} или callable-объектом."
#         )
#
#     def _collect_requires_pipeline(self) -> Generator[ContractRequire, None, None]:
#         collected_requires = []
#         collected_requires += self._collect_preprocess_requires()
#         collected_requires += self._collect_isinstance_requires()
#         collected_requires += self._collect_cls_requires()
#         collected_requires += self._collect_extra_requires()
#         assert all(
#             isinstance(require, ContractRequire) for require in collected_requires
#         ), f"Все элементы должны быть экземплярами класса {ContractRequire.__name__!r}."
#
#         return (r for r in dict.fromkeys(collected_requires))
#
#     def _collect_preprocess_requires(self) -> Generator[ContractRequire, None, None]:
#         if self._preprocess_value_before_requires is not None:
#             yield get_contract_require(
#                 obj=self._preprocess_value_before_requires,
#                 attr_name_for_raise_detail="preprocess_value_before_requires!r",
#                 description=f"Ошибка при обработке значения поля {self._name!r}.",
#             )
#
#     def _collect_isinstance_requires(self) -> Generator[ContractRequire, None, None]:
#         if self._override_isinstance_base_validator:
#             self._check_types_for_isinstance(self._override_isinstance_base_validator)
#             if not self._check_valid_require(self._override_isinstance_base_validator):
#                 TypeError(
#                     f"Атрибут 'preprocess_value_before_requires' должен быть "
#                     f"callable-объектом или {ContractRequire.__name__!r}."
#                 )
#             yield get_contract_require(
#                 obj=self._override_isinstance_base_validator,
#                 attr_name_for_raise_detail="override_isinstance_check_types!r",
#                 description=f"Ошибка при обработке значения поля {self._name!r}.",
#             )
#         elif self._check_isinstance:
#             yield get_contract_require(
#                 obj=self._current_isinstance_validator,
#                 attr_name_for_raise_detail="override_isinstance_check_types!r",
#                 description=(
#                     f"Нарушен контракт проверки типа поля {self._name!r}. "
#                     f" Ожидается {self._expected_types!r}."
#                 ),
#             )
#
#     def _collect_cls_requires(self) -> Generator[ContractRequire, None, None]:
#         for predicate in self.base_requires:
#             yield get_contract_require(
#                 obj=predicate,
#                 attr_name_for_raise_detail=f"cls {self.__class__.__name__!r} 'requires'",
#             )
#
#     def _collect_extra_requires(self) -> Generator[ContractRequire, None, None]:
#         for i, predicate in enumerate(self._extra_requires) or ():
#             yield get_contract_require(
#                 obj=predicate,
#                 attr_name_for_raise_detail=(
#                     f"Элемент в аргументе 'extra_requires'(индекс={i}) "
#                     f"метода  __init__() в классе {self.__class__.__name__!r}"
#                 ),
#             )
#
#     def _validation(self, value: T) -> T:
#         for require in self._all_requires:
#             curr_env = os.environ.get(self._env_name, None)
#             if curr_env and curr_env not in require.environments:
#                 return value
#             if not require(value):
#                 # exc = exc or ContractViolationError
#                 raise exc(
#                     f"Нарушен контракт {require.__qualname__!r} поля {self._name!r}. "
#                     f"Значение: {value!r}({type(value)!r}). Описание: {msg}."
#                 )
#         return value
#
#     def _isinstance_validator(self, value: Any) -> bool:
#         if not isinstance(value, self._expected_types):
#             try:
#                 self._expected_types(value)  # Проверка на Enum
#                 return True
#             except (ValueError,):
#                 pass
#             raise ContractViolationValueTypeError(
#                 field_name=self._name,
#                 got=value,
#                 expected=self._expected_types,
#             )
#         return True
#
#     def _isinstance_enum_validator(self, value: Any) -> bool:
#         try:
#             self._expected_types(value)
#         except ValueError:
#             raise ContractViolationValueTypeError(
#                 field_name=self._name,
#                 got=value,
#                 expected=self._expected_types,
#             )
#
#         return True
#
#     def __call__(self, value: T) -> Any:
#         if value is None:
#             if self._nullable:
#                 return None
#             raise ContractViolationValueTypeError(
#                 field_name=self._name,
#                 got=None,
#                 expected=self._expected_types,
#             )
#         if self._use_cache and (value in self._cache):
#             return value
#         try:
#             value = (
#                 self._preprocess_value_before_requires(value)
#                 if self._preprocess_value_before_requires
#                 else value
#             )
#         except Exception as e:
#             raise ContractViolationPreProcessingError(e)
#
#         self._validation(value)
#
#         if self._check_isinstance and not self._is_enum:
#             assert isinstance(value, self._expected_types), (
#                 f"Неверный тип данных после всех валидаций. Значение={value!r}. "
#                 f"Ожидается: {self._expected_types!r}. Получено {type(value)!r}."
#             )
#         if self._use_cache:
#             self._cache.add(value)
#             assert value in self._cache, "Элемент не был добавлен в кеш."
#         return value
#
#     def __repr__(self):
#         return (
#             f"{self.__class__.__name__}("
#             f"name={self._name!r} "
#             f"expected_types={self._expected_types!r} "
#             f"nullable={self._nullable!r} "
#             f"is_enum={self._is_enum!r} "
#             f"use_cache={self._use_cache!r} "
#             f"all_requires_count={len(self._all_requires)!r} "
#             f")"
#         )
#
#     @classmethod
#     def get_cache(cls) -> CacheFieldProtocol:
#         return cls._cache
#
#     @property
#     def name(self):
#         return self._name
#
#     @property
#     def default_err_message(self):
#         return f"Нарушен контракта поля {self._name!r}."



class AbstractContractField(ABC):

    _cache: CacheFieldProtocol
    base_requires: Sequence[ContractRequireProtocol] | None = None

    def __init_subclass__(cls, *, cache: CacheFieldProtocol | None = None, **kwargs):
        if cache is None:
            cls._cache = set()
        else:
            cls._cache = cache
        if cls.base_requires is None:
            cls.base_requires = ()
        for i, require in enumerate(cls.base_requires):
            if not isinstance(require, ContractRequireProtocol):
                raise TypeError(
                    f"Тип аргумента {cls.base_requires!r}' должен быть "
                    f"соответствовать протоколу {ContractRequireProtocol.__name__!r}. "
                    f"Предоставленный тип: {type(require)!r}. Индекс={i}."
                )
        super().__init_subclass__(**kwargs)


    @classmethod
    def get_cache(cls) -> CacheFieldProtocol:
        return cls._cache

    @classmethod
    def clear_cache(cls) -> CacheFieldProtocol:
        return cls._cache.clear()

    def __init__(
        self,
        *,
        field_name: str,
        nullable: bool = False,
        preprocess_value_require: Sequence[ContractPreprocessRequireProtocol] | None = None,
        requires: Sequence[ContractRequireProtocol] | None = None,
        invariants: Sequence[ContractRequireProtocol] | None = None,
        env_name: str | None = None,
        use_cache: bool | None = True,
    ):
        self._name = field_name
        self._nullable = nullable
        self._preprocess_value_requires = tuple(preprocess_value_require) if preprocess_value_require is not None else ()



        # if self._preprocess_value_requires is not None:
        #     if not isinstance(self._preprocess_value_requires, ContractPreprocessRequireProtocol):
        #         formatted_attr_name = replace_self_from_attr_name(f"{self._preprocess_value_requires=}")
        #         raise TypeError(
        #             f"Тип аргумента {formatted_attr_name!r} должен "
        #             f"соответствовать протоколу {ContractPreprocessRequireProtocol.__name__!r}. "
        #             f"Предоставленный тип: {type(self._preprocess_value_requires)!r}."
        #             f"Значение={self._preprocess_value_requires!r}"
        #         )
        self._requires = tuple(requires) if requires is not None else ()
        # for i, r in enumerate(self._requires):
        #     if not isinstance(r, ContractRequireProtocol):
        #         formatted_attr_name = replace_self_from_attr_name(f"{self._requires=}")
        #         raise TypeError(
        #             f"Тип аргумента {formatted_attr_name!r}' должен "
        #             f"соответствовать протоколу {ContractRequireProtocol.__name__!r}. "
        #             f"Предоставленный тип: {type(r)!r}."
        #             f"Значение={r!r}"
        #             f"Индекс={i}"
        #         )
        self._invariants = tuple(invariants) if invariants is not None else ()
        # for i, r in enumerate(self._invariants):
        #     if not isinstance(r, ContractRequireProtocol):
        #         formatted_attr_name = replace_self_from_attr_name(f"{self._invariants=}")
        #         raise TypeError(
        #             f"Тип аргумента {formatted_attr_name!r}' должен "
        #             f"соответствовать протоколу {ContractRequireProtocol.__name__!r}. "
        #             f"Предоставленный тип: {type(r)!r}."
        #             f"Значение={r!r}"
        #             f"Индекс={i}"
        #             )

        # to_check = [
        #     (requires, replace_self_from_attr_name(attr_data_for_exception))
        #     for requires, attr_data_for_exception in[
        #         (self._preprocess_value_requires, f"{self._preprocess_value_requires=}"),
        #         (self._requires, f"{self._requires=}"),
        #         (self._invariants, f"{self._invariants=}"),
        #     ]
        # ]

        self._check_requires_is_valid()

        self._env_name = env_name
        self._use_cache = use_cache

    def _check_requires_is_valid(self) -> None:
        to_check = [
            (requires, attr_data_as_string_for_exception)
            for requires, attr_data_as_string_for_exception in [
                (self._preprocess_value_requires, f"{self._preprocess_value_requires=}"),
                (self._requires, f"{self._requires=}"),
                (self._invariants, f"{self._invariants=}"),
            ]
        ]
        print(to_check)
        for requires, name in to_check:
            for i, require in enumerate(requires):
                if not isinstance(require, ContractRequireProtocol):
                    formatted_attr_name = replace_self_from_attr_name(name)
                    raise TypeError(
                        f"Тип аргумента {formatted_attr_name!r} должен "
                        f"соответствовать протоколу {ContractRequireProtocol.__name__!r}. "
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

    def __call__(self, value: Any) -> Any:
        if value is None:
            if self._nullable:
                return None
            raise ContractViolationFieldError(
                field_name=self._name,
                contract=f"'nullable'={self._nullable!r}",
                violation=f"Значение поля не может быть {None!r}",
                value=value,
            )
        self._check_invariants(value)
        if self._use_cache and (value in self._cache):
            return value
        if self._preprocess_value_requires:
            try:
                value = self._preprocess_value_requires(value)
            except Exception as e:
                self._check_invariants(value)
                raise ContractViolationPreProcessingError(
                    field_name=self._name,
                    contract=self._preprocess_value_requires.contract,
                    violation=self._preprocess_value_requires.violation,
                    value=value,
                    detail=self._preprocess_value_requires.detail,
                )
        self._check_invariants(value)
        value = self._validate(value)
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
            f"has_preprocess_value_require={bool(self._preprocess_value_requires)!r} "
            f"count_requires={len(self._requires)!r} "
            f"count_invariants={len(self._invariants)!r}"
            f")"
        )

    @property
    def name(self):
        return self._name


class ContractField(AbstractContractField):
    """ Базовый класс для создания контракта полей. """


class ContractIntegerField(AbstractContractField):

    def __init__(
        self,
        *,

        field_name: str,
        nullable: bool = False,
        preprocess_value_require: ContractPreprocessRequireProtocol | None = None,
        requires: Sequence[ContractRequireProtocol] | None = None,
        invariants: Sequence[ContractRequireProtocol] | None = None,
        env_name: str | None = None,
        use_cache: bool = False,
        min_value: int = 0,
        max_value: int | None = None,

    ):
        self._min_value = min_value
        self._max_value = max_value
        super().__init__(
            field_name=field_name,
            nullable=nullable,
            preprocess_value_require=preprocess_value_require,
            requires=requires,
            invariants=invariants,
            env_name=env_name,
            use_cache=use_cache,
        )

    def repr_schema(self):
        return (
            f"{super().repr_schema()} "
            f"min_value={self._min_value!r} "
            f"max_value={self._max_value!r} "
        )

    def _validate(self, value: Any) -> Any:
        err = None
        if value < self._min_value:
            err = f"Значение {value} меньше минимального {self._min_value}."
        elif value > self._max_value:
            err = f"Значение {value} больше максимального {self._max_value}."

        if err is not None:
            err_pattern = "Диапазон допустимых значений целого числа: от {} до {}"
            raise ContractViolationFieldError(
                contract=err_pattern.format(self._min_value, self._max_value),
                field_name=self._name,
                violation=err,
                value=value,
                detail="Нарушен контракт диапазона допустимых значений целого числа: от {} до {}. {}".format(
                    self._min_value, self._max_value, err
                ),
            )
        return super()._validate(value)



if __name__ == "__main__":
    contract_field = ContractField(
        field_name="test",
        nullable=False,
    )

    pos_int = ContractIntegerField(
        field_name="test2",
        min_value=0,
        max_value=10,
        nullable=False,
        use_cache=True,
        requires=['are'],
    )
    print(contract_field)
    print(pos_int(4))
    print(pos_int(5))
    print(pos_int(10))
    print(pos_int.get_cache())
    print(pos_int(()))
