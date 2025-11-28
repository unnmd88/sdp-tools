import logging

from app_logging.dev.config import PASSPORTS_OWNERS_LOGGER
from infrastructure.database.models.crud import BaseCrud
from infrastructure.database.models import PassportGroup


class PassportGroupsCrud(BaseCrud):
    model = PassportGroup
    logger = logging.getLogger(PASSPORTS_OWNERS_LOGGER)
