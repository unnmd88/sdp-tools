import functools
from collections.abc import Coroutine, Callable
from logging import Logger
from typing import Any

from sqlalchemy.exc import SQLAlchemyError

from domain.exceptions import DomainValidationError
from infrastructure.exceptions import RepositoryError


def handle_db_errors(logger: Logger = None):
    """Фабрика декораторов для обработки ошибок БД"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(self, *args, **kwargs) -> Any:
            try:
                return await func(self, *args, **kwargs)
            except SQLAlchemyError as exc:
                if logger:
                    logger.error(f"Read failed in {func.__name__}: {exc}")
                raise RepositoryError(message=f"Operation failed: {func.__name__}") from exc
        return async_wrapper
    return decorator


class HandleErrorsWrapper:
    def __init__(self, logger=None):
        self._logger: Logger = logger

    async def __call__(self, coro: Coroutine):
        try:
            return await coro
        except SQLAlchemyError as exc:
            if self._logger:
                self._logger.error(f"Read failed in {coro.__name__}: {exc}")
            raise RepositoryError(message=f"Read operation failed") from exc

