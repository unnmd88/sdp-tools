import asyncio
import logging

import bcrypt
from app_logging.dev.config import USERS_LOGGER
from core.database import db_api
from core.models import User
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.enums.organizations import Organizations
from core.enums.roles import Roles

logger = logging.getLogger(USERS_LOGGER)


async def create_user():
    pass


async def create_root(session: AsyncSession = None):
    name = 'root'
    password = bcrypt.hashpw(
        b'sdp2025',
        bcrypt.gensalt(),
    )
    user_root = User(
        first_name=name,
        last_name=name,
        username=name,
        organization=Organizations.SDP,
        password=password,
        is_active=True,
        is_admin=True,
        is_superuser=True,
        role=Roles.superuser,
        phone_number='',
        telegram='',
        description='',
    )
    sess: AsyncSession = session or db_api.session_factory()
    try:
        sess.add(user_root)
        await sess.commit()
        await sess.refresh(user_root)
        logger.info('User %r was created with id=%s.', name, user_root.id)
        return user_root
    except IntegrityError:
        logger.warning('User %r already exists.', name)
    finally:
        await sess.aclose()


if __name__ == '__main__':
    asyncio.run(create_root())
