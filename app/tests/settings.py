from starlette.testclient import TestClient

from core.config import settings
from main import app

BASE_URL = (
    f'http://{settings.run.host}:{settings.run.port}'
    f'{settings.api.prefix}{settings.api.v1.prefix}'
)

client = TestClient(
    app=app,
    base_url=BASE_URL,
)