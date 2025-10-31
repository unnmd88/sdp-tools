import httpx
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from main import app
from tests.settings import BASE_URL


# def test_invalid_username_or_password():
#     print(f'{BASE_URL}/login')
#     response = client.post(
#         f'{BASE_URL}/auth/login',
#         data={"username": "test2", "password": "123"},
#     )
#     print(response.json())
#     assert response.status_code == 200

@pytest_asyncio.fixture
async def async_client():
    # async with AsyncClient(base_url=BASE_URL) as client:
    async with AsyncClient(base_url=BASE_URL) as client:
        yield client


@pytest.mark.asyncio
async def test_async_endpoint1(async_client):

    response = await async_client.post(f'{BASE_URL}/auth/login/', data={"userna2me": "test2", "password": "1234"}, )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_async_endpoint(async_client):

    response = await async_client.post(f'{BASE_URL}/auth/login/', data={"username": "test2", "password": "1234"}, )

    print(response.json())