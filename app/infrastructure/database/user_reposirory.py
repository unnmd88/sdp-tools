import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app_logging.dev.config import INFRASTRUCTURE
from domain.users.user_entity import UserEntity
from infrastructure.database.mappers.users_mapper import UserDBMapper
from infrastructure.database.models import User as UserModel
from infrastructure.database.base_repository import BaseCrudSqlAlchemyRepositoryAdapter
from infrastructure.database.utils import async_handle_db_errors

logger = logging.getLogger(INFRASTRUCTURE)


class UsersSqlAlchemyRepository(BaseCrudSqlAlchemyRepositoryAdapter[UserModel, UserEntity]):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=UserModel, mapper=UserDBMapper())

    async def get_by_username(self, username: str) -> UserEntity | None:
        return await self.get_filter_by({"username": username})

    async def try_by_username(self, username: str) -> UserEntity | None:
        return await self.try_filter_by({"username": username})

    # async def change_password(
    #     self, user_id: int, hashed_password: bytes
    # ) -> UserEntity | None:
    #     return await self.update_with_fields(_id=user_id, password=hashed_password)
