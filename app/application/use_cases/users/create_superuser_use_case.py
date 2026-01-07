import asyncio

from core.config import settings

from core.enums import Organizations, Roles
from core.users.entities.user import UserEntity
from core.users.services.user_password import hash_password
from infrastructure.database.api import db_api
from infrastructure.database.user_reposirory import UsersRepositorySqlAlchemy


async def create_user_root(password: str = None):

    async with db_api.session_factory() as sess:
        user_repo = UsersRepositorySqlAlchemy(session=sess)
        user_root: UserEntity = UserEntity(
            first_name='root',
            last_name ='root',
            username ='root',
            organization=Organizations.SDP,
            email=None,
            password=hash_password(password or settings.default_superuser_creds.password),
            is_active=True,
            role=Roles.superuser,
            phone_number=None,
            telegram=None,
            description='Корневой пользователь системы',
        )
        created_user_root = await user_repo.add_user(user_root)
    return created_user_root

if __name__ == '__main__':
    asyncio.run(create_user_root())