from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.user import UserEntity
from infrastructure.database.mappers.users_mapper import UserDBMapper
from infrastructure.database.models import User as UserModel
from infrastructure.database.base_repository import BaseSqlAlchemyRepository


class UsersSqlAlchemyRepository:
    def __init__(self, session: AsyncSession):
        self._repo = BaseSqlAlchemyRepository[UserModel, UserEntity, UserDBMapper](
            session=session,
            model=UserModel,
            mapper=UserDBMapper(),
        )

    async def get_by_username(self, username: str) -> UserEntity | None:
        return await self._repo.get_one_or_none_by_filters(username=username)

    async def get_by_id(self, _id: int) -> UserEntity | None:
        return await self._repo.get_by_id(_id)

    async def add(self, user: UserEntity) -> UserEntity:
        return await self._repo.add(user)