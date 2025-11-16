import bcrypt
import pytest

from sqlalchemy.engine.result import Result
from sqlalchemy.sql.expression import select

from core.models import User
from core.database.api import DatabaseAPI
from users.create_root import create_root
from users.organizations import Organizations
from users.roles import Roles


@pytest.mark.asyncio(loop_scope='session')
async def test_create_user_root(t_dp_api: DatabaseAPI):

    async with t_dp_api.session_factory() as sess:
        user_root1: User = await create_root(sess)
        print('user_root1: ', user_root1)

    async with t_dp_api.session_factory() as sess:
        stmt = select(User).where(User.username == 'root')
        result: Result = await sess.execute(stmt)
        usr_root2 = result.scalars().one()
        print('usr_root2: ', usr_root2)
        passwd_is_valid = bcrypt.checkpw(
            password='sdp2025'.encode('utf-8'),
            hashed_password=usr_root2.password,
        )
        assert isinstance(user_root1, User) and isinstance(usr_root2, User)
        assert isinstance(user_root1.password, bytes) and isinstance(usr_root2.password, bytes)
        assert passwd_is_valid
        assert user_root1 == usr_root2
        assert all(getattr(user_root1, attr) == getattr(usr_root2, attr) for attr in User.__table__.columns.keys())

