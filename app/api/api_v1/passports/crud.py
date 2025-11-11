import logging

from app_logging.dev.config import OVIM_PASSPORTS_LOGGER
from core.database.crud import BaseCrud
from core.models import OvimPassport


class OvimPassportsCrud(BaseCrud):
    model = OvimPassport
    logger = logging.getLogger(OVIM_PASSPORTS_LOGGER)