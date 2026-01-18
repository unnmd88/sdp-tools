from collections.abc import Sequence, Container
from dataclasses import dataclass
from typing import Callable, Any

from domain.contracts.interfaces.require_schemas_interfaces import (
    ContractRequireSchemaProtocol,
    ContractProcessValueSchemaRequireProtocol,
)


@dataclass(kw_only=True, frozen=True, slots=True)
class ContractRequireSchema(ContractRequireSchemaProtocol):
    """
    Контейнер для описания зависимостей и условий в контрактах.

    Представляет собой неизменяемый контейнер данных, который определяет
    условие (предикат), которое должно быть выполнено для корректной работы
    контракта.

    Args:
        handler (Callable[..., bool] | Callable[[], bool]): Функция-предикат,
            проверяющая условие контракта. Должна возвращать True, если условие
            выполнено, и False в противном случае.
        detail (str): Человеко-читаемое описание условия. Используется для
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
            TypeError: Если 'detail' не является строкой.
            TypeError: Если 'custom_exception' не является экземпляром
                Exception или классом, унаследованным от Exception.
    """

    handler: Callable[..., bool]
    contract: str = ""
    violation: str = ""
    detail: str = ""
    custom_exception: Exception | type[Exception] | None = None
    environments: Container[str] | None = None

    def __post_init__(self) -> None:
        if not callable(self.handler):
            raise TypeError("Аргумент 'handler' должен быть callable-объектом.")
        if not isinstance(self.detail, str):
            raise TypeError("Аргумент 'detail' должен быть строкой.'")
        if isinstance(self.custom_exception, Exception):
            return
        if isinstance(self.custom_exception, type) and not issubclass(
            Exception, self.custom_exception
        ):
            raise TypeError(
                f"Аргумент 'custom_exception' должен быть подклассом "
                f"{Exception.__name__!r} или экземпляром подкласса."
            )

    def __call__(self, *args, **kwargs) -> bool:
        return self.handler(*args, **kwargs)


@dataclass(kw_only=True, frozen=True, slots=True)
class ContractProcessValueRequireSchema(ContractProcessValueSchemaRequireProtocol):
    handler: Callable[[Any], Any]
    contract: str = ""
    violation: str = ""
    detail: str = ""
    custom_exception: Exception | type[Exception] | None = None
    environments: Container[str] | None = None

    def __call__(self, *args, **kwargs) -> Any:
        return self.handler(*args, **kwargs)
