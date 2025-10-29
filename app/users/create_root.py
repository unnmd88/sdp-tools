import asyncio

from core.models import db_api

from users import crud as crud_users
from users.organizations import Organizations
from users.roles import Roles
from users.schemas import CreateUser


async def create_root():
    name = 'root'
    password = 'sdp2025'
    user = CreateUser(
        first_name=name,
        last_name=name,
        username=name,
        organization=Organizations.spetsdorproject,
        password=password,
        is_active=True,
        is_admin=True,
        is_superuser=True,
        role=Roles.superuser,
        phone_number='',
        telegram='',
        description='',
    )
    async with db_api.session_factory() as session:
        res = await crud_users.create_user(user=user, sess=session, from_app=True)

    return res


if __name__ == '__main__':
    asyncio.run(create_root())
