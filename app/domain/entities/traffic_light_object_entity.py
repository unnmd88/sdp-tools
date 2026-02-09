from domain.entities.base_entity import Entity

"""
Поля:
    - id: int primary key
    - region: reference to region. RegionEntity
    - name : string номер светофора
    - type_controller: str VO тип контроллера
    - district: str VO округ
    - address: str VO адрес
    - service_organization: str VO обслуживающая организация
    - main_mode: str VO основной режим работы
    - coordinates: VO tuple[float latitude, float longitude] координаты
    - status: str текущий статус
    - network: VO str сетевые настройки+оборудование
    - description: str описание
    - updated_at: datetime
    - created_at: datetime
    
    Перспективные поля:
    - peripheral: list[str] VO периферийных устройств(КИП-Д, Moxa, ...)
    
    
"""


class TrafficLightObjectEntity(Entity):
    """ Сущность светофорного объекта. """