import pytest

from core.config import settings
from core.models import Base
from core.models.database_api import DatabaseAPI
from main import app
from starlette.testclient import TestClient

BASE_URL = (
    f'http://{settings.run.host}:{settings.run.port}'
    f'{settings.api.prefix}{settings.api.v1.prefix}'
)

client = TestClient(
    app=app,
    base_url=BASE_URL,
)

@pytest.fixture(scope='session')
def t_dp_api():
    yield DatabaseAPI(
        url='postgresql+asyncpg://admin2:1111@localhost:5433/db_test',
        echo=True,
        echo_pool=True,
        pool_size=50,
        max_overflow=10,
    )


@pytest.fixture(scope='session')
async def t_session(t_dp_api):
    async with t_dp_api.session_factory() as session:
        yield session
    await t_dp_api.dispose()


@pytest.fixture(scope='session', autouse=True)
async def create_tables(t_dp_api):
    async with t_dp_api.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



