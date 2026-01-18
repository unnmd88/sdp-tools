from typing import Any

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from domain.exceptions.crud import CreateErrorAlreadyExists
from domain.users.entities.user import UserEntity
from infrastructure.database.api import db_api
from infrastructure.database.mappers.users_mapper import UserDBMapper
from infrastructure.database.models import User
from infrastructure.database.base_repository import BaseSqlAlchemy, Entity


class UsersRepositorySqlAlchemy(BaseSqlAlchemy):
    model = User
    mapper = UserDBMapper

    async def add_user(self, entity: UserEntity) -> Entity | None:
        new_instance = self.mapper.to_model(entity)
        self.session.add(new_instance)
        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e
        return self.mapper.to_entity(new_instance)

    async def get_user_by_id_or_username_or_none(
        self, username_or_id: int | str
    ) -> UserEntity | None:
        if isinstance(username_or_id, int):
            return await self.get_one_by_id_or_none(username_or_id)
        stmt = select(self.model).filter_by(username=username_or_id)
        res = await self.session.execute(stmt)
        if (user := res.scalars().one_or_none()) is not None:
            return self.mapper.to_entity(user)
        return None
