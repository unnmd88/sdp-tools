import logging
from collections.abc import Sequence
from contextlib import asynccontextmanager
from dataclasses import asdict
from typing import TypeVar, TypeAlias, Type

from sqlalchemy import select, delete
from sqlalchemy.engine.result import Result
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, OperationalError, DBAPIError
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import update

from app_logging.dev.config import INFRASTRUCTURE
from application.interfaces.mappers.db import BaseDBMapperProtocol
from infrastructure.exceptions import RepositoryError, RepositoryUpdateError, RepositoryIntegrityError, \
    RepositoryConnectionError

EntityType = TypeVar("EntityType")
ModelType = TypeVar("ModelType")
CreateDTOType = TypeVar("CreateDTOType")

# class BaseSqlAlchemy:
#     model = T
#     mapper: BaseDBMapperProtocol
#
#     def __init__(self, session: AsyncSession):
#         self.session: AsyncSession = session
#
#     async def get_by_id(self, _id: int) -> Entity | None:
#         if (model := await self.session.get(self.model, _id)) is not None:
#             return self.mapper.to_entity(model)
#         return None
#
#     async def get_one_or_none_by_filters(self, filters: dict) -> Entity | None:
#         stmt = select(self.model).filter_by(**filters)
#         result = await self.session.execute(stmt)
#         if (model := result.scalars().one_or_none()) is not None:
#             return self.mapper.to_entity(model)
#         return None
#
#     async def get_many(self, filters: dict = None) -> Sequence[Entity]:
#         stmt = select(self.model).filter_by(**filters if filters else {})
#         result = await self.session.execute(stmt)
#         return [self.mapper.to_entity(model) for model in result.scalars().all()]
#
#     # async def get_all(self, **filters) -> Sequence[Entity]:
#     #     stmt = select(self.model).filter_by(**filters)
#     #     result = await self.session.execute(stmt)
#     #     return [self.mapper.to_entity(model) for model in result.scalars().all()]
#
#     async def add(self, create_record_dto: CreateRecordDTO) -> Entity | None:
#         entity = self.mapper.entity_validate(
#             **create_record_dto.fields
#         )  # Возможно исключение DomainValidationError
#         search_filters = (
#             create_record_dto.check_exists_search_filters or create_record_dto.fields
#         )
#         stmt = select(self.model).filter_by(**search_filters)
#         result: Result = await self.session.execute(stmt)
#         if result.scalars().one_or_none() is not None:
#             raise CreateErrorAlreadyExists
#         new_instance = self.mapper.to_model(entity)
#
#         self.session.add(new_instance)
#         try:
#             await self.session.commit()
#             return self.mapper.to_entity(new_instance)
#         except IntegrityError:
#             await self.session.rollback()
#             raise CreateErrorAlreadyExists
#         except SQLAlchemyError as e:
#             await self.session.rollback()
#             raise e
#
#     async def update_one(
#         self,
#         update_record_dto: ToUpdateRecordDTO,
#     ):
#         stmt = select(self.model).filter_by(**update_record_dto.search_criteria)
#         result: Result = await self.session.execute(stmt)
#         if (current_model := result.scalars().one_or_none()) is None:
#             raise EntityNotFoundError
#         old_entity = self.mapper.to_entity(current_model)
#         # Создать инстанс сущности для проверки валидности обновляемых полей
#         updated_fields = asdict(old_entity) | update_record_dto.fields
#         self.mapper.entity_validate(
#             **updated_fields
#         )  # Возможно исключение DomainValidationError
#
#         # stmt = (
#         #     update(self.model)
#         #     .where(self.model.id == current_model.id)
#         #     .values(update_record_dto.fields)
#         #     .returning("*")
#
#         try:
#             for k, v in update_record_dto.fields.items():
#                 setattr(current_model, k, v)
#             await self.session.commit()
#             updated_entity = await self.get_one_or_none_by_filters(
#                 {"id": old_entity.id}
#             )
#             return UpdatedRecordDTO(
#                 old_entity, updated_entity, name=self.model.__name__
#             )
#         except SQLAlchemyError as e:
#             raise
#
#     # async def update(
#     #     self,
#     #     _id: int,
#     #     **fields,
#     # ) -> UpdatedRecordDTO:
#     #     if (current_model := await self.session.get(self.model, _id)) is None:
#     #         raise NotFoundError
#     #     old_entity = self.mapper.to_entity(current_model)
#     #     try:
#     #         for k, v in fields.items():
#     #             setattr(current_model, k, v)
#     #         await self.session.commit()
#     #         updated_entity = self.mapper.to_entity(current_model)
#     #         return UpdatedRecordDTO(old_entity, updated_entity, name=self.model.__name__)
#     #     except SQLAlchemyError as e:
#     #         raise UpdateError(e)
#
#     async def delete_one(self, delete_record_dto: DeleteRecordDTO) -> Entity | None:
#         entity = await self.get_one_or_none_by_filters(delete_record_dto.search_filters)
#         if entity is None:
#             raise EntityNotFoundError
#         stmt = delete(self.model).filter_by(id=entity.id)
#         try:
#             await self.session.execute(stmt)
#             await self.session.commit()
#             if (await self.get_one_or_none_by_filters({"id": entity.id})) is not None:
#                 raise DeleteError
#         except SQLAlchemyError as e:
#             raise DeleteError(e)
#         return entity
#
#     # async def update(
#     #     self,
#     #     _id: int,
#     #     **fields,
#     # ):
#     #     stmt = select(self.model).filter_by(id=_id)
#     #     result: Result = await self.session.execute(stmt)
#     #     model = result.scalars().one()
#     #     try:
#     #         for k, v in fields.items():
#     #             if v is not None:
#     #                 setattr(model, k, v)
#     #         await self.session.commit()
#     #     except SQLAlchemyError as e:
#     #         await self.session.rollback()
#     #         raise e
#     #     return model

logger = logging.getLogger(INFRASTRUCTURE)


class BaseSqlAlchemyRepository[ModelType, EntityType, CreateDTOType]:
    """Базовый репозиторий для работы с базой данных через sqlalchemy."""

    def __init__(
        self,
        *,
        session: AsyncSession,
        model: Type[ModelType],
        mapper: BaseDBMapperProtocol,
        default_filters: dict | None = None,
    ):
        self._session = session
        self._model = model
        self._mapper = mapper
        self._default_filters = default_filters or {}

    async def get_by_id(self, _id: int) -> EntityType | None:
        if (model := await self._session.get(self._model, _id)) is not None:
            return self._mapper.to_entity(model)
        return None

    async def get_one_or_none_by_filters(self, **filters) -> EntityType | None:
        stmt = select(self._model).filter_by(**filters)
        result = await self._session.execute(stmt)
        if (model := result.scalars().one_or_none()) is not None:
            return self._mapper.to_entity(model)
        return None

    async def get_many(
        self,
        skip: int = 0,
        limit: int | None = None,
        order_by: list | None = None,
        **filters
    ) -> list[EntityType]:
        stmt = select(self._model).filter_by(**filters)

        if order_by:
            stmt = stmt.order_by(*order_by)
        if skip:
            stmt = stmt.offset(skip)
        if limit:
            stmt = stmt.limit(limit)

        result = await self._session.execute(stmt)
        return [self._mapper.to_entity(model) for model in result.scalars()]

    async def add(self, entity: EntityType) -> EntityType:
        instance = self._mapper.to_model(entity)
        try:
            self._session.add(instance)
            await self._session.flush()
            await self._session.refresh(instance)
            return self._mapper.to_entity(instance)
        except IntegrityError as e:
            text = str(e.orig)
            if "DETAIL" in text:
                msg = text.split("DETAIL:")[1].strip()  # todo: убрать это костыль
            else:
                msg = ""
            raise RepositoryIntegrityError(
                private_message=str(e),
                public_message=msg
            )
        except (OperationalError, DBAPIError) as e:
            if "connection" in str(e).lower() or "lost" in str(e).lower():
                await self._session.invalidate()
            raise RepositoryConnectionError(private_message=str(e))
        except SQLAlchemyError as e:
            raise RepositoryError(private_message="Ошибка при работе с базой данных")
        except Exception:  # todo logging
            raise RepositoryError(private_message="Ошибка при работе с базой данных")

    async def update(self, id: int, **fields) -> EntityType | None:
        stmt = select(self._model).filter_by(id=id).with_for_update()
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            return None

        for key, value in fields.items():
            if hasattr(model, key):
                setattr(model, key, value)
            else:
                logger.error(f"У модели {self._model.__name__} отсутствует атрибут {key}")
                exc = RepositoryError(private_message=f"У модели {self._model.__name__} отсутствует атрибут {key}")
                raise exc

        try:
            await self._session.flush()
            await self._session.refresh(model)
            return self._mapper.to_entity(model)
        except IntegrityError as e:
            raise RepositoryIntegrityError(original_error=e)
        except (OperationalError, DBAPIError) as e:
            if "connection" in str(e).lower() or "lost" in str(e).lower():
                await self._session.invalidate()
            raise RepositoryConnectionError(private_message=str(e))
        except SQLAlchemyError as e:
            raise RepositoryError(private_message="Ошибка при работе с базой данных")
        except Exception:  # todo logging
            raise RepositoryError(private_message="Ошибка при работе с базой данных")

    # async def update(self, id: int, **fields) -> EntityType | None:
    #     try:
    #         stmt = (
    #             update(self._model)
    #             .where(self._model.id == id)
    #             .values(**fields)
    #             .returning(self._model)
    #         )
    #         result = await self._session.execute(stmt)
    #         model = result.scalar_one_or_none()
    #         await self._session.commit()
    #         if model is not None:
    #             return self._mapper.to_entity(model)
    #         return None
    #     except IntegrityError as e:
    #         raise RepositoryIntegrityError(original_error=e)
    #     except (OperationalError, DBAPIError) as e:
    #         raise RepositoryConnectionError(private_message=e)
    #     except SQLAlchemyError as e:
    #         raise RepositoryError(private_message="Ошибка при работе с базой данных")
    #     except Exception:  # todo logging
    #         raise RepositoryError(private_message="Ошибка при работе с базой данных")