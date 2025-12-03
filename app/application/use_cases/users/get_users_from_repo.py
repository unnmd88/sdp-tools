from application.interfaces.services.get_user import UsersCrudRepositoryProtocol
from core.users._schemas import UserFromDbFullSchema


class UsersRepositoryUseCaseImpl:
    def __init__(self, user_service: UsersCrudRepositoryProtocol):
        self.user_service = user_service

    async def get_user_by_username(self, username: str) -> UserFromDbFullSchema:
        return await self.user_service.get_user_by_username_or_none(username)

    async def get_user_by_id(self, user_id: int) -> UserFromDbFullSchema:
        return await self.user_service.get_user_by_id_or_none(user_id)
