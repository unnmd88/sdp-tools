from application.interfaces.repositories.base import BaseCrudProtocol


class BaseCrudUseCaseImpl:

    def __init__(self, repository: BaseCrudProtocol):
        self.repository = repository

    async def get_one_by_id(self, entity_id):
        return await self.repository.get_one_by_id(entity_id)

    async def get_all(self):
        ...