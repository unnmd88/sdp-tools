from application.interfaces.repositories.base import BaseRepositoryProtocol


class GetByIdUseCase:

    def __init__(self, repository: BaseRepositoryProtocol):
        self.repository = repository

    async def get_by_id(self, _id: int):
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

class GetRegionByIdUseCase(BaseRepositoryProtocol):
    def __init__(self, repository: BaseRepositoryProtocol):