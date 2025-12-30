from collections.abc import Sequence
from dataclasses import asdict
from typing import TypeVar, TypeAlias, Any

from sqlalchemy import select, update, delete
from sqlalchemy.engine.result import Result
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio.session import AsyncSession

from application.interfaces.mappers.db import BaseDBMapperProtocol
from application.interfaces.repositories.base import BaseCrudProtocol, FiltersForSearchProtocol
from core.dto.common import CreateRecordDTO, UpdatedRecordDTO, ToUpdateRecordDTO, DeleteRecordDTO
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

    async def get_one_or_none_by_filters(self, filters: dict) -> Entity | None:
        stmt = select(self.model).filter_by(**filters)
        result = await self.session.execute(stmt)
        if (model := result.scalars().one_or_none()) is not None:
            return self.mapper.to_entity(model)
        return None

    async def get_many(self, filters: dict = None) -> Sequence[Entity]:
        stmt = select(self.model).filter_by(**filters if filters else {})
        result = await self.session.execute(stmt)
        return [self.mapper.to_entity(model) for model in result.scalars().all()]


    # async def get_all(self, **filters) -> Sequence[Entity]:
    #     stmt = select(self.model).filter_by(**filters)
    #     result = await self.session.execute(stmt)
    #     return [self.mapper.to_entity(model) for model in result.scalars().all()]


    async def add(self, create_record_dto: CreateRecordDTO) -> Entity | None:
        entity = self.mapper.entity_validate(**create_record_dto.fields) # Возможно исключение DomainValidationError
        search_filters = create_record_dto.check_exists_search_filters or create_record_dto.fields
        stmt = select(self.model).filter_by(**search_filters)
        result: Result = await self.session.execute(stmt)
        if result.scalars().one_or_none() is not None:
            raise CreateErrorAlreadyExists
        new_instance = self.mapper.to_model(entity)
        self.session.add(new_instance)
        try:
            await self.session.commit()
            return self.mapper.to_entity(new_instance)
        except IntegrityError:
            await self.session.rollback()
            raise CreateErrorAlreadyExists
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e

    async def update_one(
        self,
        update_record_dto: ToUpdateRecordDTO,
    ):
        stmt = select(self.model).filter_by(**update_record_dto.search_filters)
        result: Result = await self.session.execute(stmt)
        if (current_model := result.scalars().one_or_none()) is None:
            raise NotFoundError
        old_entity = self.mapper.to_entity(current_model)

        updated_fields = asdict(old_entity) | update_record_dto.fields
        updated_entity = self.mapper.entity_validate(**updated_fields) # Возможно исключение DomainValidationError

        try:
            for k, v in update_record_dto.fields.items():
                setattr(current_model, k, v)
            await self.session.commit()
            # updated_entity = self.mapper.to_entity(current_model)
            return UpdatedRecordDTO(old_entity, updated_entity, name=self.model.__name__)
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
    ) -> UpdatedRecordDTO:
        if (current_model := await self.session.get(self.model, _id)) is None:
            raise NotFoundError
        old_entity = self.mapper.to_entity(current_model)
        try:
            for k, v in fields.items():
                setattr(current_model, k, v)
            await self.session.commit()
            updated_entity = self.mapper.to_entity(current_model)
            return UpdatedRecordDTO(old_entity, updated_entity, name=self.model.__name__)
        except SQLAlchemyError as e:
            raise UpdateError(e)

    async def delete_one(self, delete_record_dto: DeleteRecordDTO) -> Entity | None:

        stmt = select(self.model).filter_by(**delete_record_dto.search_filters)
        result: Result = await self.session.execute(stmt)
        if (current_model := result.scalars().one_or_none()) is None:
            raise NotFoundError
        stmt = delete(self.model).filter_by(id=current_model.id)
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

