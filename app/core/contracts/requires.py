from dataclasses import dataclass
from typing import Callable


@dataclass(kw_only=True, frozen=True, slots=True)
class ContractRequire:
    """
    Контейнер для описания зависимостей и условий в контрактах.

    Представляет собой неизменяемый контейнер данных, который определяет
    условие (предикат), которое должно быть выполнено для корректной работы
    контракта.

    Args:
        predicate (Callable[..., bool] | Callable[[], bool]): Функция-предикат,
            проверяющая условие контракта. Должна возвращать True, если условие
            выполнено, и False в противном случае.
        description (str): Человеко-читаемое описание условия. Используется для
            формирования понятных сообщений об ошибках и логирования.
            По умолчанию: пустая строка.
        custom_exception (Exception | type[Exception] | None): Пользовательское
            исключение или класс исключения, который будет выброшен при нарушении
            условия. Если None, будет использовано исключение по умолчанию.
            По умолчанию: None.

    Особенности:
        - Реализует протокол итератора для распаковки атрибутов.
    Raises:
            TypeError: Если 'predicate' не является callable-объектом.
            TypeError: Если 'description' не является строкой.
            TypeError: Если 'custom_exception' не является экземпляром
                Exception или классом, унаследованным от Exception.
    """

    predicate: Callable[..., bool] | Callable[[], bool]
    description: str = ""
    custom_exception: Exception | type[Exception] = None

    def __iter__(self):
        return (el for el in (self.predicate, self.description, self.custom_exception))

    def __post_init__(self) -> None:
        if not callable(self.predicate):
            raise TypeError("Аргумент 'predicate' должен быть callable-объектом.")
        if not isinstance(self.description, str):
            raise TypeError("Аргумент 'description должен быть строкой.'")
        if isinstance(self.custom_exception, Exception):
            return
        if isinstance(self.custom_exception, type) and not issubclass(
            Exception, self.custom_exception
        ):
            raise TypeError(
                f"Аргумент 'custom_exception' должен быть подклассом "
                f"{Exception.__name__!r} или экземпляром подкласса."
            )
