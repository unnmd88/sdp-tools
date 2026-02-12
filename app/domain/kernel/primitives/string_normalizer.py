import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import Self

#
# @dataclass(slots=True, frozen=True)
# class StringNormalizer:
#
#     _WHITESPACE = re.compile(r'\s+')
#
#     __slots__ = ("_value", )
#
#     def __init__(self, value: str) -> None:
#         self._value = value
#
#     @classmethod
#     def normalize_of(cls, string: str) -> Self:
#         return cls(string)
#
#     def strip(self) -> Self:
#         self._value = self._value.strip()
#         return self
#
#     def normalize_whitespace(self) -> Self:
#         """Множественные пробелы → один пробел."""
#         self._value = re.sub(self._WHITESPACE, " ", self._value)
#         return self
#
#     def remove_all_whitespace(self) -> Self:
#         """Удалить ВСЕ пробелы, табы, переносы."""
#         self._value = re.sub(self._WHITESPACE, "", self._value)
#         return self
#
#     def capitalize(self) -> Self:
#         """ Привести первую букву к верхнему регистру. """
#         self._value = self._value.capitalize()
#         return self
#
#     def lower(self) -> Self:
#         """ Привести к нижнему регистру. """
#         self._value = self._value.lower()
#         return self
#
#     def upper(self) -> Self:
#         """ Привести к верхнему регистру. """
#         self._value = self._value.upper()
#         return self
#
#     def replace(self, old: str, new: str) -> Self:
#         """Заменить подстроку."""
#         self._value = self._value.replace(old, new)
#         return self
#
#     def regex_replace(self, pattern: str | re.Pattern, replacement: str) -> Self:
#         """Заменить по regex."""
#         self._value = re.sub(pattern, replacement, self._value)
#         return self
#
#     def map(self, func: Callable[[str], str]):
#         """ Применить функцию к строке. """
#         self._value = func(self._value)
#         return self
#
#     def get(self):
#         """Получить нормализованную строку."""
#         return self._value
#
#     def __repr__(self) -> str:
#         return self._value


@dataclass(slots=True, frozen=True)
class StringNormalizer:

    _WHITESPACE = re.compile(r'\s+')

    value: str

    @classmethod
    def normalize_of(cls, string: str) -> Self:
        return cls(string)

    def strip(self) -> Self:
        return self.__class__(self.value.strip())

    def normalize_whitespace(self) -> Self:
        """Множественные пробелы → один пробел."""
        return self.__class__(re.sub(self._WHITESPACE, " ", self.value))

    def remove_all_whitespace(self) -> Self:
        """Удалить ВСЕ пробелы, табы, переносы."""
        return self.__class__(re.sub(self._WHITESPACE, "", self.value))

    def capitalize(self) -> Self:
        """ Привести первую букву к верхнему регистру. """
        return self.__class__(self.value.capitalize())

    def lower(self) -> Self:
        """ Привести к нижнему регистру. """
        return self.__class__(self.value.lower())

    def upper(self) -> Self:
        """ Привести к верхнему регистру. """
        return self.__class__(self.value.upper())

    def replace(self, old: str, new: str) -> Self:
        """Заменить подстроку."""
        return self.__class__(self.value.replace(old, new))

    def regex_replace(self, pattern: str | re.Pattern, replacement: str) -> Self:
        """Заменить по regex."""
        return self.__class__(re.sub(pattern, replacement, self.value))

    def map(self, func: Callable[[str], str]) -> Self:
        """ Применить функцию к строке. """
        return self.__class__(func(self.value))

    def transform(self, *funcs: Callable[[str], str]) -> Self:
        """Применить несколько преобразований за один вызов."""
        result = self.value
        for func in funcs:
            result = func(result)
        return self.__class__(result)

    def get(self):
        """Получить нормализованную строку."""
        return self.value

    def __repr__(self) -> str:
        return self.value


if __name__ == '__main__':
    s = StringNormalizer('   hello world   ')
    print(s)
    res = s.strip().capitalize().map(lambda x: x.upper()).get()
    print(res)
    nws = '   hello world   '.strip().capitalize().upper()

