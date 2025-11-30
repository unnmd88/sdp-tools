import pytest
from core.config import settings
from core.database import DatabaseAPI
from core.models import Base, User
from main import app
from starlette.testclient import TestClient
from core.users import users as user_examples

BASE_URL = (
    f'http://{settings.run.host}:{settings.run.port}'
    f'{settings.api.prefix}{settings.api.v1.prefix}'
)

FILL_DATA_TO_TABLES_DB = True

client = TestClient(
    app=app,
    base_url=BASE_URL,
)


@pytest.fixture(scope='session')
def t_dp_api():
    yield DatabaseAPI(
        url='postgresql+asyncpg://test1:1111@192.168.200.3:5432/test',
        echo=True,
        echo_pool=True,
        pool_size=50,
        max_overflow=10,
    )


# @pytest.fixture(scope='session')


@pytest.fixture(scope='session')
async def t_session(t_dp_api):
    async with t_dp_api.session_factory() as session:
        yield session
    await t_dp_api.dispose()


# @pytest.fixture(scope='session', autouse=True)
# async def create_tables(
#     t_dp_api,
# ):
#     async with t_dp_api.engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#     async with t_dp_api.engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     if FILL_DATA_TO_TABLES_DB:
#         async with t_dp_api.session_factory() as session:
#             try:
#                 session.add_all(users_models())
#                 await session.commit()
#                 session.add_all(regions_models())
#                 await session.commit()
#                 session.add_all(traffic_light_objects())
#                 await session.commit()
#                 session.add_all(passports_owners_models())
#                 await session.commit()
#                 session.add_all(passports_models())
#                 await session.commit()
#             except SQLAlchemyError:
#                 await session.rollback()
#                 raise
#     yield


@pytest.fixture
async def preparing_clean_database(
    t_dp_api,
):
    async with t_dp_api.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    async with t_dp_api.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest.fixture
def user_models():
    return [User(**u) for u in user_examples]


# @pytest.fixture
# def regions_model_instances():
#     return [
#         Region(code=77, name='Москва'),
#         Region(code=78, name='Питер'),
#         Region(code=69, name='Тверь'),
#         Region(code=65, name='Сахалин'),
#     ]


# @pytest.fixture(autouse=True)
# async def crete_regions():
#     d = DatabaseAPI(
#         url='postgresql+asyncpg://admin2:1111@localhost:5433/db_test',
#         echo=True,
#         echo_pool=True,
#         pool_size=50,
#         max_overflow=10,
#     )
#
#     async with d.session_factory() as session:
#         session.add_all(
#             [
#                 Region(code=77, name='Москва'),
#                 Region(code=78, name='Питер'),
#                 Region(code=69, name='Тверь'),
#                 Region(code=65, name='Сахалин'),
#             ]
#         )
#         await session.commit()
