from sqlalchemy import select

from core.users.schemas import UserFromDbFullSchema
from infrastructure.database.api import db_api
from infrastructure.database.models import User
from infrastructure.database.base_repository import BaseSqlAlchemy


class UsersRepositorySqlAlchemy(BaseSqlAlchemy):

    model = User

    async def get_user_by_username_or_none(self, username: str) -> UserFromDbFullSchema | None:
        async with db_api.session_factory() as session:
            stmt = select(self.model).filter_by(username=username)
            res = await session.execute(stmt)
            user = res.scalars().one_or_none()
        print(f'User: {user}')
        if user is not None:
            return UserFromDbFullSchema.model_validate(user, from_attributes=True)
        return None


    # async def get_user_by_id_or_404(
    #     self,
    #     # session: AsyncSession,
    #     user_id: Annotated[int, Field(ge=1)],
    # ):
    #     if (res := await session.get(User, user_id)) is None:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail=f'User with id={user_id} not found',
    #         )
    #     return UserFromDbFullSchema.model_validate(res)