from core.config import settings
from infra.database.api import DatabaseAPI

# from core.database import DatabaseAPI

db_api_helper = DatabaseAPI(url=str(settings.db.url))
