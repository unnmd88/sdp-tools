import asyncio

from sqlalchemy import Result
from sqlalchemy.sql.expression import update, select

from core.models import User, TrafficLightObject
from core.database.api import DatabaseAPI


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


users = [
    {
        'first_name': 'Gimmo',
        'last_name': 'Gimmo',
        'username': 'Gimmo',
        'organization': 'Spetsdorproject',
        'email': 'user@example.com',
        'password': b'1234',
        'is_active': True,
        'is_admin': True,
        'is_superuser': True,
        'role': 'superuser',
        'phone_number': '',
        'telegram': '',
        'description': 'Тестовый юзер 2',
    },
    # {
    #     'first_name': 'Test',
    #     'last_name': 'Testov',
    #     'username': 'test1',
    #     'organization': 'Spetsdorproject',
    #     'email': 'user@example.com',
    #     'password': b'1234',
    #     'is_active': True,
    #     'is_admin': True,
    #     'is_superuser': True,
    #     'role': 'superuser',
    #     'phone_number': '',
    #     'telegram': '',
    #     'description': 'Тестовый юзер 1',
    # },
    # {
    #     'first_name': 'Test1',
    #     'last_name': 'Testov1',
    #     'username': 'test2',
    #     'organization': 'Spetsdorproject',
    #     'email': 'user@example.com',
    #     'password': b'1234',
    #     'is_active': True,
    #     'is_admin': True,
    #     'is_superuser': True,
    #     'role': 'superuser',
    #     'phone_number': '',
    #     'telegram': '',
    #     'description': 'Тестовый юзер 2',
    # },
]


async def search():
    async with t_dp_api.session_factory() as session:
        stmt = select(User).where(User.username.in_(['test1', 'test2']))
        result: Result = await session.execute(stmt)
        print(result.scalars().all())


async def create_users():
    async for session in t_dp_api.session_getter_commit():
        session.add_all([User(**u) for u in users])


async def create_traffic_light_objects():
    objects = [
        TrafficLightObject(
            region=1,
            name='laba_test',
            district='ЦАО',
            street='BAZA BEREG'

        )
    ]
    async for session in t_dp_api.session_getter_commit():
        session.add_all(objects)


async def main():
    # await search()
    # await create_users()
    await create_traffic_light_objects()


if __name__ == '__main__':
    asyncio.run(main())
