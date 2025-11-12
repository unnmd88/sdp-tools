import logging
from collections.abc import Sequence
from typing import TypeVar

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.exceptions import NotFoundByIdException
from core.models import Base


T = TypeVar('T', bound=Base)


class BaseCrud[T]:
    model: type[T]
    logger: logging.Logger = logging.getLogger(__name__)

    def __init__(
        self,
        a_session: AsyncSession,
    ) -> None:
        self.a_session = a_session

    @classmethod
    async def get_one_by_id_or_404(cls, session: AsyncSession, pk_id: int) -> T:
        if (res := await session.get(cls.model, pk_id)) is None:
            raise NotFoundByIdException(
                entity_name=cls.model.__name__,
                num_id=pk_id,
            )
        return res

    @classmethod
    async def get_all(
        cls, session: AsyncSession, filters: BaseModel = None
    ) -> Sequence[T]:
        if filters:
            filter_dict = filters.model_dump(exclude_unset=True)
        else:
            filter_dict = {}
        query = select(cls.model).filter_by(**filter_dict)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def add(cls, session: AsyncSession, model: BaseModel):
        new_instance = cls.model(**model.model_dump(exclude_unset=True))
        cls.logger.info(
            'Попытка добавить строку в таблицу %r из данных %r',
            cls.model.__name__, model
        )
        session.add(new_instance)
        try:
            await session.commit()
            cls.logger.info( 'Новая запись добавлена успешно: %r', new_instance)
        except IntegrityError:
            cls.logger.warning('Новая запись не была добавлена: данные уже существуют')
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f'Already exists.',
            )
        except SQLAlchemyError as e:
            cls.logger.error('Ошибка добавления данных: %r', e)
            await session.rollback()
            raise e
        return new_instance


    @classmethod
    async def update(
            cls,
            session: AsyncSession,
            db_model: T,
            update_model: BaseModel,
            exclude_unset: bool = True,
    ) -> T:
        try:
            for k, v in update_model.model_dump(exclude_unset=exclude_unset).items():
                setattr(db_model, k, v)
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return db_model
