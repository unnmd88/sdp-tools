import asyncio

from sqlalchemy.sql.expression import update

from core.models import db_api, User


async def main():

    async with db_api.session_factory() as session:
        stmt = (
        update(User)
        .where(User.id == 1)
        .values(telegram="@patrick")
        )
        await session.execute(stmt)
        await session.commit()


if __name__ == '__main__':
    asyncio.run(main())