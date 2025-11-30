from application.interfaces.repositories.users import UsersRepositoryProtocol
from core.users.schemas import UserFromDbFullSchema


class UsersCrudUseCase:

    def __init__(self, repository: UsersRepositoryProtocol):
        self.repository = repository

    async def get_one_by_id(self, entity_id) -> UserFromDbFullSchema | None:
        return await self.repository.get_one_by_id_or_none(entity_id)

    async def get_all(self):
        ...