import logging

from app_logging.dev.config import PASSPORTS_OWNERS_LOGGER
from infra.database.models.crud import BaseCrud
from infra.database import PassportGroup


class PassportGroupsCrud(BaseCrud):
    model = PassportGroup
    logger = logging.getLogger(PASSPORTS_OWNERS_LOGGER)
