from core.database.crud import BaseCrud
from core.models import TrafficLightObject


class TloCrud(BaseCrud):
    model = TrafficLightObject
