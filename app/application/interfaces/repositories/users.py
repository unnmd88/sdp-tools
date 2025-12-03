from application.interfaces.repositories.base import BaseCrudProtocol


class UsersCrudRepositoryProtocol(BaseCrudProtocol):

    async def get_user_by_username_or_none(self, username: str): ...
