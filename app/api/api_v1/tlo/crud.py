from core.database.crud import BaseCrud
from core.models import TrafficLightObject, Region


class TloCrud(BaseCrud):
    model = TrafficLightObject
