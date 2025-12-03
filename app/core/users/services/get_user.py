from core.users.exceptions import UserNotFoundException
from core.users._schemas import UserFromDbFullSchema
from infrastructure.database.user_reposirory import UsersRepositorySqlAlchemy


class UserServiceImpl:
    repository_factory = UsersRepositorySqlAlchemy

    def __init__(self, provider):
        self.repository = self.repository_factory('12321')

    async def get_user_by_username_or_none(self, username: str) -> UserFromDbFullSchema:
        if (
            user := await self.repository.get_user_by_username_or_none(username)
        ) is None:
            raise UserNotFoundException(username)
        print(user)
        return user

    async def get_user_by_id_or_none(self, user_id: int) -> UserFromDbFullSchema:
        if (user := await self.repository.get_one_by_id_or_none(user_id)) is None:
            raise UserNotFoundException(user_id)
        print(user)
        return user


# class UserServiceImpl:
#     repository_factory = UsersRepositorySqlAlchemy
#
#     def __init__(self):
#         self.repository = self.repository_factory('12321')
#
#     async def get_user_by_username_or_none(self, username: str) -> UserFromDbFullSchema:
#         if (
#             user := await self.repository.get_user_by_username_or_none(username)
#         ) is None:
#             raise UserNotFoundException(username)
#         print(user)
#         return user
#
#     async def get_user_by_id_or_none(self, user_id: int) -> UserFromDbFullSchema:
#         if (user := await self.repository.get_one_by_id_or_none(user_id)) is None:
#             raise UserNotFoundException(user_id)
#         print(user)
#         return user
