from collections.abc import Iterable


class StringNormalizer:
    def __init__(
        self,
        *,
        strip: bool = True,
        lowercase: bool = False,
        from_iterable=False,
        from_iterable_delimiter: str = " ",
        capitalize: bool = False,
        uppercase: bool = False,
    ) -> None:
        self._from_iterable_delimiter = from_iterable_delimiter
        self._processors = []
        if from_iterable:
            self._processors.append(self._join)
        if strip:
            self._processors.append(str.strip)
        if lowercase:
            self._processors.append(str.lower)
        if uppercase:
            self._processors.append(str.upper)
        if capitalize:
            self._processors.append(str.capitalize)

    def __call__(self, value: Iterable) -> str:
        for processor in self._processors:
            value = processor(value)
        return value

    def _join(self, _iterable: Iterable) -> str:
        return self._from_iterable_delimiter.join(str(v) for v in _iterable)


class Normalizer:
    @classmethod
    def normalize_phone_number(cls, value: str) -> str:
        """Нормализация номера телефона до 10 цифр без знака +."""
        value = value.replace("+", "")
        if len(value) == 10:
            return value
        if len(value) == 11 and value.startswith("7"):
            return value[1:]
        else:
            raise ValueError("Invalid phone number")


if __name__ == "__main__":
    s = StringNormalizer(lowercase=True, from_iterable=True, from_iterable_delimiter="")
    print(s(("hello", "world")))
    print(s("Ouuueee"))
