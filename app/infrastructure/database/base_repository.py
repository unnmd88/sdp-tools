from collections.abc import Sequence
from typing import TypeVar, TypeAlias, Any

from sqlalchemy import select, update, delete
from sqlalchemy.engine.result import Result
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio.session import AsyncSession

from application.interfaces.mappers.db import BaseDBMapperProtocol
from application.interfaces.repositories.base import BaseCrudProtocol
from core.dto.update_entity import UpdatedEntityDTO
from core.exceptions.base import CreateError, CreateErrorAlreadyExists, NotFoundError, UpdateError, DeleteError
from core.regions.entities.region import RegionEntity
from core.tlo.entities.tlo import TrafficLightObjectEntity
from core.users.entities.user import UserEntity
from core.users.exceptions import UserAlreadyExistsException
from infrastructure.database.models import Base
from infrastructure.database.api import db_api
from fastapi.params import Depends


T = TypeVar('T', bound=type[Base])
Entity: TypeAlias = UserEntity | TrafficLightObjectEntity | RegionEntity
Record = TypeVar('Record', bound=Base)


class BaseSqlAlchemy:
    model = T
    mapper: BaseDBMapperProtocol

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get_one_by_id_or_none(self, _id: int) -> Entity | None:
        if (model := await self.session.get(self.model, _id)) is not None:
            return self.mapper.to_entity(model)
        return None

    async def get_one_or_none_by_filters(self, **filters) -> Entity | None:
        stmt = select(self.model).filter_by(**filters)
        result = await self.session.execute(stmt)
        if (model := result.scalars().one_or_none()) is not None:
            return self.mapper.to_entity(model)
        return None


    async def get_all(self, **filters) -> Sequence[Entity]:
        stmt = select(self.model).filter_by(**filters)
        result = await self.session.execute(stmt)
        return [self.mapper.to_entity(model) for model in result.scalars().all()]


    async def add(self, entity) -> Entity | None:
        new_instance = self.mapper.to_model(entity)
        # cls.logger.info(
        #     'Попытка добавить строку в таблицу %r из данных %r',
        #     cls.model.__name__,
        #     model,
        # )
        self.session.add(new_instance)
        try:
            await self.session.commit()
            print(f'ENTITY: {self.mapper.to_entity(new_instance)}')
            return self.mapper.to_entity(new_instance)
            # cls.logger.info('Новая запись добавлена успешно: %r', new_instance)
        except IntegrityError:
            # cls.logger.warning('Новая запись не была добавлена: данные уже существуют')
            await self.session.rollback()
            raise CreateErrorAlreadyExists
        except SQLAlchemyError as e:
            # cls.logger.error('Ошибка добавления данных: %r', e)
            await self.session.rollback()
            raise e
        return None

    async def update_one(
        self,
        filters: dict,
        **fields,
    ):
        stmt = select(self.model).filter_by(**filters)
        result: Result = await self.session.execute(stmt)
        if (current_model := result.scalars().one_or_none()) is None:
            raise NotFoundError
        old_entity = self.mapper.to_entity(current_model)
        try:
            for k, v in fields.items():
                setattr(current_model, k, v)
            await self.session.commit()
            updated_entity = self.mapper.to_entity(current_model)
            return UpdatedEntityDTO(old_entity, updated_entity, name=self.model.__name__)
        except SQLAlchemyError as e:
            raise UpdateError(e)
        # stmt = (
        #     update(self.model)
        #     .filter_by(**filters)
        #     .values(**fields)
        #     .returning("*")
        # )

        try:
            for k, v in fields.items():
                if v is not None:
                    setattr(model, k, v)
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e
        return model

    async def update(
        self,
        _id: int,
        **fields,
    ) -> UpdatedEntityDTO:
        if (current_model := await self.session.get(self.model, _id)) is None:
            raise NotFoundError
        old_entity = self.mapper.to_entity(current_model)
        try:
            for k, v in fields.items():
                setattr(current_model, k, v)
            await self.session.commit()
            updated_entity = self.mapper.to_entity(current_model)
            return UpdatedEntityDTO(old_entity, updated_entity, name=self.model.__name__)
        except SQLAlchemyError as e:
            raise UpdateError(e)

    async def delete_one(self, _id: int):
        if (current_model := await self.session.get(self.model, _id)) is None:
            raise NotFoundError
        stmt = delete(self.model).filter_by(id=_id)
        entity = self.mapper.to_entity(current_model)
        try:
            await self.session.execute(stmt)
            await self.session.commit()
        except SQLAlchemyError as e:
            raise DeleteError(e)
        return entity


    # async def update(
    #     self,
    #     _id: int,
    #     **fields,
    # ):
    #     stmt = select(self.model).filter_by(id=_id)
    #     result: Result = await self.session.execute(stmt)
    #     model = result.scalars().one()
    #     try:
    #         for k, v in fields.items():
    #             if v is not None:
    #                 setattr(model, k, v)
    #         await self.session.commit()
    #     except SQLAlchemyError as e:
    #         await self.session.rollback()
    #         raise e
    #     return model

