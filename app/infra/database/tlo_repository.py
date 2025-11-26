from infra.database import TrafficLightObject
from infra.database.base_repository import BaseSqlAlchemy


class TrafficLightObjectSqlAlchemy(BaseSqlAlchemy):

    model = TrafficLightObject