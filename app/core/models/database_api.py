import functools
from collections.abc import AsyncGenerator, Callable
from typing import Any

import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from core.config import settings


class DatabaseAPI:
    def __init__(
        self,
        url: str,
        echo: bool = False,
        echo_pool: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
    ):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        await self.engine.dispose()
        # log.info("Database engine disposed")

    def base_session_getter(
        self,
        commit: bool = False,
        rollback: bool = False,
    ):
        async def wrapper():
            async with self.session_factory() as session:
                try:
                    print('BEFORE yield session!' * 100)
                    yield session
                    if commit:
                        await session.commit()
                    print('AFTER yield session!' * 100)
                except Exception:  # todo logging
                    if rollback:
                        await session.rollback()
                finally:
                    await session.close()
                    with open('lllog.log', 'a+') as f:
                        f.write('NEW GEN!' * 100)

        return wrapper

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session

    async def session_getter_commit(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session
            await session.commit()

    async def session_getter_commit_and_rollback_if_err(
        self,
    ) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:  # todo logging
                await session.rollback()


db_api = DatabaseAPI(
    url=str(settings.db.url),
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)


def async_session_factory(commit: bool = True, rollback: bool = True):
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            async with db_api.session_factory() as session:
                try:
                    return await func(*args, session=session, **kwargs)
                except Exception:  # todo logging
                    if rollback:
                        await session.rollback()
                finally:
                    if commit:
                        await session.commit()

        return wrapped

    return wrapper
