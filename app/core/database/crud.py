import logging
from collections.abc import Sequence
from typing import TypeVar, Annotated

from fastapi import HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.models import Base, User
from users.schemas import UserFromDbFullSchema

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
    async def get_user_by_id_or_404(
        cls,
        session: AsyncSession,
        user_id: Annotated[int, Field(ge=1)],
    ):
        if (res := await session.get(User, user_id)) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'User with id={user_id} not found',
            )
        return UserFromDbFullSchema.model_validate(res)

    @classmethod
    async def get_pk_id_from_model_or_404(
        cls,
        session: AsyncSession,
        from_model: type[T],
        **filters,
    ) -> int:
        res = await session.execute(select(from_model.id).filter_by(**filters))
        if (pk_id := res.scalar_one_or_none()) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    f'Instance of {from_model.__class__.__name__!r} '
                    f'with filters {" ".join(f"{k!r}={v!r}" for k, v in filters.items())} '
                    f'not found'
                ),
            )
        return pk_id

    @classmethod
    async def get_one_by_id_or_404(cls, session: AsyncSession, pk_id: int) -> T:
        if (res := await session.get(cls.model, pk_id)) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(f'{cls.model.__name__!r} with pk_id {pk_id!r} not found '),
            )
        return res

    @classmethod
    async def get_all(
        cls,
        session: AsyncSession,
        filters: BaseModel = None,
    ) -> Sequence[T]:
        if filters:
            filter_dict = filters.model_dump(exclude_unset=True)
        else:
            filter_dict = {}
        query = select(cls.model).filter_by(**filter_dict)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def add(
        cls,
        session: AsyncSession,
        model: BaseModel,
    ):
        new_instance = cls.model(**model.model_dump(exclude_unset=True))
        cls.logger.info(
            'Попытка добавить строку в таблицу %r из данных %r',
            cls.model.__name__,
            model,
        )
        session.add(new_instance)
        try:
            await session.commit()
            cls.logger.info('Новая запись добавлена успешно: %r', new_instance)
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
        to_update_model: BaseModel,
        exclude_unset: bool = True,
    ) -> T:
        try:
            for k, v in to_update_model.model_dump(exclude_unset=exclude_unset).items():
                setattr(db_model, k, v)
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return db_model
