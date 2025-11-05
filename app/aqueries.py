import asyncio

from sqlalchemy import Result
from sqlalchemy.sql.expression import update, select

from core.models import db_api, User
from core.models.database_api import DatabaseAPI


# def t_dp_api():
#     return DatabaseAPI(
#         url='postgresql+asyncpg://admin2:1111@localhost:5433/db_test',
#         echo=True,
#         echo_pool=True,
#         pool_size=50,
#         max_overflow=10,
#     )


t_dp_api = DatabaseAPI(
    url='postgresql+asyncpg://admin2:1111@localhost:5433/db_test',
    echo=True,
    echo_pool=True,
    pool_size=50,
    max_overflow=10,
)


async def update_telegram():
    async with db_api.session_factory() as session:
        stmt = update(User).where(User.id == 1).values(telegram='@patrick')
        await session.execute(stmt)
        await session.commit()


async def search():
    async with t_dp_api.session_factory() as session:
        stmt = select(User).where(User.username.in_(['test1', 'test2']))
        result: Result = await session.execute(stmt)
        print(result.scalars().all())


async def main():
    await search()


if __name__ == '__main__':
    asyncio.run(main())
