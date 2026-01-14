from abc import ABC, abstractmethod
from collections.abc import Sequence
from enum import Enum

from types import UnionType
from typing import (
    Callable,
    Any,
    Iterable, )

from core.contracts.custom_types import AcceptRequireTypeAsTuple
from core.contracts.exc import (
    ContractViolationError,
    ContractViolationPreProcessingError,
    ContractViolationValueTypeError, ContractViolationInvariantError,
)
from core.contracts.interfaces.cahe_interface import CacheFieldProtocol
from core.contracts.interfaces.require import ContractRequireProtocol
from core.contracts.utils import create_contract_require

type RequireTypeData = ContractRequireProtocol | Callable[..., bool]
type IsInstanceType = type | tuple[type, ...] | UnionType | Enum


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

    _cache: CacheFieldProtocol = None
    base_requires: Sequence[ContractRequireProtocol] = None

    def __init_subclass__(cls, *, cache: CacheFieldProtocol = None, **kwargs):
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
            cls.base_requires = tuple(create_contract_require(r) for r in cls.base_requires)

        # if cls.expected_types and issubclass(cls.expected_types, Enum):
        #     cls._is_enum_cls_ = True
        # cls._check_types_for_isinstance(cls.expected_types)
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
        name: str,
        nullable: bool = False,
        expected_types: IsInstanceType = None,
        preprocess: ContractRequireProtocol | Callable[..., bool] | AcceptRequireTypeAsTuple = None,
        requires: Sequence[ContractRequireProtocol | Callable[..., bool] | AcceptRequireTypeAsTuple] = None,
        invariant: ContractRequireProtocol | Callable[..., bool] | AcceptRequireTypeAsTuple = None,
        env_name: str = None,
        use_cache: bool = True,
    ):
        self._name = name
        self._nullable = nullable
        self._expected_types = expected_types
        self._preprocess_value_before_requires = preprocess
        self._requires = requires or ()
        self._invariant = invariant
        self._env_name = env_name
        self._use_cache = use_cache

    @abstractmethod
    def validate(self, value: Any) -> Any:
        ...

    def __call__(self, value: Any) -> Any:
        if value is None:
            if self._nullable:
                return None
            raise ContractViolationValueTypeError(
                field_name=self._name,
                got=None,
                expected=self._expected_types,
            )
        if self._use_cache and (value in self._cache):
            return value
        if self._preprocess_value_before_requires:
            try:
                value = self._preprocess_value_before_requires(value)
            except Exception as e:
                raise ContractViolationPreProcessingError(
                    self._preprocess_value_before_requires.description or e,
                )
        if self._expected_types and not self.type_check(value):
            raise ContractViolationValueTypeError(
                field_name=self._name,
                got=value,
                expected=self._expected_types,
            )

        value = self.validate(value)

        if self._use_cache:
            self._cache.add(value)
            assert value in self._cache, "Элемент не был добавлен в кеш."
        if self._invariant is not None and not self._invariant(value):
            raise ContractViolationInvariantError()
        return value

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"name={self._name!r} "
            f"nullable={self._nullable!r} "
            f"expected_types={self._expected_types!r} "
            f"use_cache={self._use_cache!r} "
            # f"all_requires_count={len(self._all_requires)!r} "
            f")"
        )

    def type_check(self, value: Any) -> bool:
        if isinstance(value, self._expected_types):
            return True
        if issubclass(self._expected_types, Enum):
            return True
        return False

    @property
    def name(self):
        return self._name


class ContractField(AbstractContractField):

    def validate(self, value: Any) -> Any:
        for require in self._requires:
            if not require(value):
                msg = require.description or ""
                exc = require.exc or ContractViolationError
                raise exc(
                    f"Ошибка валидации поля {self._name!r}. "
                    f"Значение: {value!r}({type(value)!r}). Описание: {msg}."
                )
        return value




# class ContractField[T]:
#
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
#         self,
#         *,
#         name: str,
#         use_cache: bool,
#         nullable: bool = None,
#         check_isinstance: bool = True,
#         preprocess_value_before_requires: ContractRequireProtocol = None,
#         override_self_expected_types: IsInstanceType = None,
#         override_isinstance_base_validator: ContractRequireProtocol = None,
#         extra_requires: Iterable[ContractRequireProtocol] = (),
#         env_name: str = None,
#         level: ValidationLevels = ValidationLevels.strict,
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
#                 self._expected_types(value) # Проверка на Enum
#                 return True
#             except (ValueError, ):
#                 pass
#             raise ContractViolationValueTypeError(
#                 arg_name=self._name,
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
#                 arg_name=self._name,
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
#                 arg_name=self._name,
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
#             f"is_enum={self._is_enum!r } "
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


class ContractEnumField(ContractField):
    _is_enum_cls_ = True

# class ContractFieldId(ContractField):
#     _name_by_default = 'id'
#     _expected_types = int
#     _requires = [ContractRequire(predicate=id_validator)]
#
#     __slots__ = ContractField.__slots__
#
#
# class ContractFieldCreatedAt(ContractField):
#     _name_by_default = 'created_at'
#     _expected_types = datetime
#     _nullable_by_default = True
#
#     __slots__ = ContractField.__slots__
#
#
# class ContractFieldUpdatedAt(ContractField):
#     _name_by_default = 'updated_at'
#     _expected_types = datetime
#     _nullable_by_default = True
#
#     __slots__ = ContractField.__slots__


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


if __name__ == "__main__":
    # print(id_field_contract)

    c = ContractField(
        name="id",
        expected_types=int,
        nullable=False,
    )
    print(c(1))
    print(c.get_cache())
    print(c(2))
    print(c(3))
    print(c(2))
    print(c.get_cache())
    print(c(None))
    c.clear_cache()
    print(c.get_cache())
