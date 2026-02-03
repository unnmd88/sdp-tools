import functools
from collections.abc import Coroutine, Callable
from logging import Logger
from typing import Any

from domain.exceptions import DomainValidationError
from infrastructure.exceptions import RepositoryCorruptedError


def async_handle_corrupted_data_in_repo(logger: Logger = None):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(self, *args, **kwargs) -> Any:
            try:
                return await func(self, *args, **kwargs)
            except DomainValidationError as exc:
                new_exc = RepositoryCorruptedError(
                    private_message=f"Нарушены данные в репозитории. "
                            f"Вероятно ручное вмешательство и корректировка данных в репозитории. "
                            f"Данные о проваленной валидации: {exc.to_dict()}."
                )
                if logger:
                    logger.error(new_exc)
                raise new_exc from exc
        return async_wrapper
    return decorator