from infrastructure.database.models import TrafficLightObject
from infrastructure.database.base_repository import BaseSqlAlchemy


class TrafficLightObjectSqlAlchemy(BaseSqlAlchemy):

    model = TrafficLightObject