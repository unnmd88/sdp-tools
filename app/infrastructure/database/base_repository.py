import logging
from collections.abc import Callable
from typing import TypeVar, Type, Any

from sqlalchemy import select

from sqlalchemy.exc import IntegrityError, SQLAlchemyError, OperationalError, DBAPIError
from sqlalchemy.ext.asyncio.session import AsyncSession


from app_logging.dev.config import INFRASTRUCTURE
from application.interfaces.mappers.db import BaseDBMapperProtocol
from domain.exceptions import DomainEntityNotFoundError
from infrastructure.database.utils import async_handle_db_errors
from infrastructure.exceptions import (
    RepositoryError,
    RepositoryIntegrityError,
    RepositoryConnectionError,
    RepositoryCorruptedError,
)

# EntityType = TypeVar("EntityType")
# ModelType = TypeVar("ModelType")
# CreateDTOType = TypeVar("CreateDTOType")


logger = logging.getLogger(INFRASTRUCTURE)


class BaseCrudSqlAlchemyRepositoryAdapter[ModelType, EntityType]:
    """Базовый репозиторий для работы с базой данных через sqlalchemy."""

    def __init__(
        self,
        *,
        session: AsyncSession,
        model: Type[ModelType],
        mapper: BaseDBMapperProtocol,
    ):
        self._session = session
        self._model = model
        self._mapper = mapper

    @property
    def mapper(self) -> BaseDBMapperProtocol:
        return self._mapper

    @async_handle_db_errors(logger=logger)
    async def try_by_id(self, _id: int) -> EntityType | None:
        if (model := await self._session.get(self._model, _id)) is not None:
            return self._mapper.to_entity(model)
        return None

    @async_handle_db_errors(logger=logger)
    async def get_by_id(self, _id: int) -> EntityType:
        if (model := await self._session.get(self._model, _id)) is not None:
            return self._mapper.to_entity(model)
        raise DomainEntityNotFoundError(
            private_message=f"Сущность {EntityType.__name__} с ID={_id} не найдена.",
        )

    @async_handle_db_errors(logger=logger)
    async def try_filter_by(self, filters: dict) -> EntityType | None:
        stmt = select(self._model).filter_by(**filters)
        result = await self._session.execute(stmt)
        if (model := result.scalars().one_or_none()) is not None:
            return self._mapper.to_entity(model)
        return None

    @async_handle_db_errors(logger=logger)
    async def get_filter_by(self, filters: dict) -> EntityType:
        stmt = select(self._model).filter_by(**filters)
        result = await self._session.execute(stmt)
        if (model := result.scalars().one_or_none()) is not None:
            return self._mapper.to_entity(model)
        raise DomainEntityNotFoundError(
            private_message=(
                f"Сущность {EntityType.__name__} не найдена. "
                f"Критерии поиска: {filters}. stmt: select(self._model).filter_by(**filters) "
            ),
        )

    @async_handle_db_errors(logger=logger)
    async def _get_model_with_wait_for(self, _id: int) -> ModelType:
        stmt = select(self._model).filter_by(id=_id).with_for_update()
        result = await self._session.execute(stmt)
        if (model := result.scalar_one_or_none()) is None:
            raise DomainEntityNotFoundError(
                private_message=f"Сущность {EntityType.__name__} с ID={_id} не найдена.",
            )
        return model

    @async_handle_db_errors(logger=logger)
    async def get_many(
        self,
        skip: int = 0,
        limit: int | None = None,
        order_by: list | None = None,
        **filters,
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

    # async def add(self, entity: EntityType) -> EntityType:
    #     instance = self._mapper.to_model(entity)
    #     try:
    #         self._session.add(instance)
    #         await self._session.flush()
    #         await self._session.refresh(instance)
    #         return self._mapper.to_entity(instance)
    #     except IntegrityError as e:
    #         text = str(e.orig)
    #         if "DETAIL" in text:
    #             msg = text.split("DETAIL:")[1].strip()  # todo: убрать это костыль
    #         else:
    #             msg = ""
    #         raise RepositoryIntegrityError(private_message=str(e), public_message=msg)
    #     except (OperationalError, DBAPIError) as e:
    #         if "connection" in str(e).lower() or "lost" in str(e).lower():
    #             await self._session.invalidate()
    #         raise RepositoryConnectionError(private_message=str(e))
    #     except SQLAlchemyError as e:
    #         raise RepositoryError(private_message="Ошибка при работе с базой данных")
    #     except Exception:  # todo logging
    #         raise RepositoryError(private_message="Ошибка при работе с базой данных")

    @async_handle_db_errors(logger=logger)
    async def add(self, entity: EntityType) -> EntityType:
        instance = self._mapper.to_model(entity)
        self._session.add(instance)
        await self._session.flush()
        await self._session.refresh(instance)
        return self._mapper.to_entity(instance)

    # async def update_with_fields(self, _id: int, **fields) -> EntityType | None:
    #     model = await self._get_model_with_wait_for(_id)
    #     for key, value in fields.items():
    #         if hasattr(model, key):
    #             setattr(model, key, value)
    #         else:
    #             logger.error(
    #                 f"У модели {self._model.__name__} отсутствует атрибут {key}"
    #             )
    #             exc = RepositoryError(
    #                 private_message=f"У модели {self._model.__name__} отсутствует атрибут {key}"
    #             )
    #             raise exc
    #     try:
    #         await self._session.flush()
    #         await self._session.refresh(model)
    #         return self._mapper.to_entity(model)
    #     except IntegrityError as e:
    #         raise RepositoryIntegrityError(original_error=e)
    #     except (OperationalError, DBAPIError) as e:
    #         if "connection" in str(e).lower() or "lost" in str(e).lower():
    #             await self._session.invalidate()
    #         raise RepositoryConnectionError(private_message=str(e))
    #     except SQLAlchemyError as e:
    #         raise RepositoryError(private_message="Ошибка при работе с базой данных")
    #     except Exception:  # todo logging
    #         raise RepositoryError(private_message="Ошибка при работе с базой данных")

    @async_handle_db_errors(logger=logger)
    async def update(self, entity: EntityType) -> EntityType | None:
        model = await self.try_by_id(entity.id)
        if model is None:
            exc = RepositoryCorruptedError(
                private_message=(
                    f"Не найдена запись в базе данных по id из "
                    f"существующей сущности {entity.__class__.__name__}, полученной из БД"
                )
            )
            logger.critical(exc.to_dict())
            raise exc
        updated_model = self.mapper.update_model(model=model, entity=entity)
        await self._session.flush()
        await self._session.refresh(updated_model)
        return self.mapper.to_entity(updated_model)

    # async def update(self, entity: EntityType) -> EntityType | None:
    #     model = await self.try_by_id(entity.id)
    #     if model is None:
    #         exc = RepositoryCorruptedError(
    #             private_message=(
    #                 f"Не найдена запись в базе данных по id из "
    #                 f"существующей сущности {entity.__class__.__name__}, полученной из БД"
    #             )
    #         )
    #         logger.critical(exc.to_dict())
    #         raise exc
    #     updated_model = self.mapper.update_model(model=model, entity=entity)
    #     await self._session.flush()
    #     await self._session.refresh(updated_model)
    #     return self.mapper.to_entity(updated_model)

    @async_handle_db_errors(logger=logger)
    async def delete(self, _id: int) -> EntityType:
        model = await self.get_by_id(_id)
        entity = self._mapper.to_entity(model)
        await self._session.delete(model)
        await self._session.flush()
        return entity
