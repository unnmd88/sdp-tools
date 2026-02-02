import functools
from collections.abc import Coroutine, Callable
from logging import Logger
from typing import Any

from application.exceptions import ApplicationLayerError
from domain.exceptions import DomainValidationError, DomainEntityNotFoundError
from infrastructure.exceptions import RepositoryError


def handle_crud_errors_from_repo(
    logger: Logger = None,
    raise_if_not_found: bool = False,
):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(self, *args, **kwargs) -> Any:
            try:
                entity = await func(self, *args, **kwargs)
                if entity is None and raise_if_not_found:
                    raise DomainEntityNotFoundError
                return entity
            except DomainValidationError as exc:
                if logger:
                    logger.error(exc)
                raise ApplicationLayerError(message=f"Нарушены данные в репозитории.") from exc
            except RepositoryError as exc:
                raise ApplicationLayerError(message=f"Ошибка репозитория: {str(exc)}") from exc
        return async_wrapper
    return decorator