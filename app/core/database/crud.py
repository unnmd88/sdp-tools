import logging
from collections.abc import Sequence
from typing import TypeVar, Annotated

from fastapi import HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.api_v1.passports.schemas import CurrentPassportSchema
from core.constants import PassportGroupsRoutes as PassportGroupsRoutesEnum
from core.models import (
    Base,
    User,
    TrafficLightObject,
    PassportGroup, Passport
)
from users.schemas import UserFromDbFullSchema

T = TypeVar('T', bound=Base)


def create_current_passport_schema_or_404(
    db_rows_from_mappings: Sequence[dict],
):
    if not db_rows_from_mappings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Current passport not found',
        )
    elif len(db_rows_from_mappings) == 1:
        if db_rows_from_mappings[0]['editing_now']:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Current passport not found, but'
                       f'editing now by user={db_rows_from_mappings[0]['username']}',
            )

        return CurrentPassportSchema(**db_rows_from_mappings[0])
    elif len(db_rows_from_mappings) == 2:
        first, second = db_rows_from_mappings[0], db_rows_from_mappings[1]
        if first['editing_now']:
            return CurrentPassportSchema(
            tlo_name=second['tlo_name'],
            username=second['username'],
            passport_group_name=second['passport_group_name'],
            data=second['data'],
            commit_message=second['commit_message'],
            editing_now={'editing_now_by_user': first['username']},
            started_editing_at=second['started_editing_at'],
            finished_editing_at=second['finished_editing_at'],
            )
        return CurrentPassportSchema(
            tlo_name=first['tlo_name'],
            username=first['username'],
            passport_group_name=first['passport_group_name'],
            data=first['data'],
            commit_message=first['commit_message'],
            editing_now=first['editing_now'],
            started_editing_at=first['started_editing_at'],
            finished_editing_at=first['finished_editing_at'],
            )


class BaseCrud[T]:
    model: type[T]
    logger: logging.Logger = logging.getLogger(__name__)

    def __init__(
        self,
        a_session: AsyncSession,
    ) -> None:
        self.a_session = a_session

    @classmethod
    async def get_tlo_and_passport_group(
        cls,
        session: AsyncSession,
        tlo_name: str,
        group_name_route: PassportGroupsRoutesEnum,
    ):
        stmt = (select(
            Passport.user_id.label('passport_user_id'),
            TrafficLightObject.id.label('tlo_id'),
            TrafficLightObject.name.label('tlo_name'),
            PassportGroup.id.label('passport_group_id'),
            PassportGroup.group_name.label('passport_group_name'),

            Passport.id.label('passport_id'),
            Passport.tlo_id,
            Passport.data,
            Passport.commit_message,
            Passport.editing_now,
            Passport.started_editing_at,
            Passport.finished_editing_at,

            User.username.label('username'),
        )
        .where(
            TrafficLightObject.name == tlo_name,
            PassportGroup.group_name_route == group_name_route,
            Passport.tlo_id == TrafficLightObject.id,
            # User.id == User.id,
            # Passport.editing_now == False,
            User.id == Passport.user_id,
            Passport.group_id == PassportGroup.id,
            )
        .order_by(Passport.finished_editing_at.desc())
        .limit(2)
         )

        result = await session.execute(stmt)
        # m = result.mappings().all()
        m = result.mappings().all()
        print(f'>>>>m: {m}')
        return create_current_passport_schema_or_404(m)
        return m

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
        res= await session.execute(
            select(from_model.id)
            .filter_by(**filters)
        )
        if (pk_id := res.scalar_one_or_none()) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    f'Instance of {from_model.__class__.__name__!r} '
                    f'with filters {" ".join(f'{k!r}={v!r}' for k, v in filters.items())} '
                    f'not found'
                ),
            )
        return pk_id

    @classmethod
    async def get_one_by_id_or_404(
            cls,
            session: AsyncSession,
            pk_id: int
    ) -> T:
        if (res := await session.get(cls.model, pk_id)) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    f'{cls.model.__name__!r} with pk_id {pk_id!r} not found '
                ),
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
