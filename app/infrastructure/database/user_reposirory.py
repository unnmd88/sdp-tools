import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import update

from app_logging.dev.config import INFRASTRUCTURE
from domain.entities.user import UserEntity
from infrastructure.database.mappers.users_mapper import UserDBMapper
from infrastructure.database.models import User as UserModel
from infrastructure.database.base_repository import BaseSqlAlchemyRepository
from infrastructure.database.utils import handle_db_errors

logger = logging.getLogger(INFRASTRUCTURE)


class UsersSqlAlchemyRepository:
    def __init__(self, session: AsyncSession):
        self._repo = BaseSqlAlchemyRepository[UserModel, UserEntity, UserDBMapper](
            session=session,
            model=UserModel,
            mapper=UserDBMapper(),
        )
        self._session = session

    @handle_db_errors(logger=logger)
    async def get_by_username(self, username: str) -> UserEntity | None:
        return await self._repo.get_one_or_none_by_filters(username=username)

    @handle_db_errors(logger=logger)
    async def get_by_username(self, username: str) -> UserEntity | None:
        return await self._repo.get_one_or_none_by_filters(username=username)

    @handle_db_errors(logger=logger)
    async def get_user_by_filters(self, **filters) -> UserEntity | None:
        return await self._repo.get_one_or_none_by_filters(**filters)

    @handle_db_errors(logger=logger)
    async def get_by_id(self, _id: int) -> UserEntity | None:
        return await self._repo.get_by_id(_id)

    @handle_db_errors(logger=logger)
    async def add(self, user: UserEntity) -> UserEntity:
        return await self._repo.add(user)

    @handle_db_errors(logger=logger)
    async def change_password(self, user_id: int, hashed_password: bytes) -> UserEntity | None:
        return await self._repo.update(id=user_id, password=hashed_password)
