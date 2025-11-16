import logging

from app_logging.dev.config import PASSPORTS_OWNERS_LOGGER
from core.database.crud import BaseCrud
from core.models import PassportGroup


class PassportGroupsCrud(BaseCrud):
    model = PassportGroup
    logger = logging.getLogger(PASSPORTS_OWNERS_LOGGER)
