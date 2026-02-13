import functools
from collections.abc import Coroutine, Callable
from logging import Logger
from typing import Any

from sqlalchemy.exc import IntegrityError, SQLAlchemyError, OperationalError, DBAPIError

from domain.exceptions import DomainValidationError
from infrastructure.exceptions import (
    RepositoryError,
    RepositoryIntegrityError,
    RepositoryConnectionError,
    RepositoryCorruptedError,
)

def async_handle_db_errors(logger: Logger = None):
    """Фабрика декораторов для обработки ошибок БД"""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(self, *args, **kwargs) -> Any:
            try:
                return await func(self, *args, **kwargs)
            except DomainValidationError as exc:
                new_exc = RepositoryCorruptedError(
                    private_message=f"Нарушены данные в репозитории. "
                    f"Вероятно ручное вмешательство и  ручная корректировка в БД. "
                )
                if logger:
                    logger.error(new_exc.to_dict())
                raise new_exc from exc
            except IntegrityError as e:
                text = str(e.orig)
                if "DETAIL" in text:
                    msg = text.split("DETAIL:")[1].strip()  # todo: убрать это костыль
                else:
                    msg = ""
                raise RepositoryIntegrityError(private_message=str(e), public_message=msg)
            except (OperationalError, DBAPIError) as e:
                if "connection" in str(e).lower() or "lost" in str(e).lower():
                    await self._session.invalidate()
                raise RepositoryConnectionError(private_message=str(e))
            except SQLAlchemyError as e:
                raise RepositoryError(private_message="Ошибка при работе с базой данных") from e
            except Exception as e:  # todo logging
                raise RepositoryError(private_message="Ошибка при работе с базой данных") from e
            # except SQLAlchemyError as exc:
            #     if logger:
            #         logger.error(f"Read failed in {func.__name__}: {exc}")
            #     raise RepositoryError(
            #         private_message=f"Operation failed: {func.__name__}"
            #     ) from exc

        return async_wrapper
    return decorator


