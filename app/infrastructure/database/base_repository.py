from collections.abc import Sequence
from typing import TypeVar, TypeAlias

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio.session import AsyncSession

from application.interfaces.mappers.db import BaseDBMapperProtocol
from application.interfaces.repositories.base import BaseCrudProtocol
from core.tlo.entities.tlo import TrafficLightObjectEntity
from core.users.entities.user import UserEntity
from core.users.exceptions import UserAlreadyExistsException
from infrastructure.database.models import Base
from infrastructure.database.api import db_api
from fastapi.params import Depends


T = TypeVar('T', bound=type[Base])
Entity: TypeAlias = UserEntity | TrafficLightObjectEntity
Record = TypeVar('Record', bound=Base)


class BaseSqlAlchemy(BaseCrudProtocol):
    model = T
    mapper: BaseDBMapperProtocol

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get_one_by_id_or_none(self, _id: int) -> Entity | None:
        if (model := await self.session.get(self.model, _id)) is not None:
            return self.mapper.to_entity(model)
        return None

    async def get_all(self, **filters) -> Sequence[Entity]:
        # if filters:
        #     filter_dict = filters.model_dump(exclude_unset=True)
        # else:
        #     filter_dict = {}
        stmt = select(self.model).filter_by(**filters)
        result = await self.session.execute(stmt)
        return [self.mapper.to_entity(model) for model in result.scalars().all()]
        return result.scalars().all()

    async def add(self, entity) -> Entity:
        new_instance = self.mapper.to_model(entity)
        # cls.logger.info(
        #     'Попытка добавить строку в таблицу %r из данных %r',
        #     cls.model.__name__,
        #     model,
        # )
        self.session.add(new_instance)
        try:
            await self.session.commit()
            # cls.logger.info('Новая запись добавлена успешно: %r', new_instance)
        except IntegrityError:
            # cls.logger.warning('Новая запись не была добавлена: данные уже существуют')
            await self.session.rollback()
            # raise UserAlreadyExistsException
        except SQLAlchemyError as e:
            # cls.logger.error('Ошибка добавления данных: %r', e)
            await self.session.rollback()
            raise e
        return new_instance

    async def update(self, model): ...
