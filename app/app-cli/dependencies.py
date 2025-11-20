from core.config import settings
from core.database.api import DatabaseAPI


db_api_helper = DatabaseAPI(url=str(settings.db.url))