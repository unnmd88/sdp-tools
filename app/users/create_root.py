import asyncio
import logging

import bcrypt

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app_logging.dev.config import USERS_LOGGER
from core.models import db_api, User

from users.organizations import Organizations
from users.roles import Roles


logger = logging.getLogger(USERS_LOGGER)


async def create_root(session: AsyncSession = None):
    name = 'root'
    password = bcrypt.hashpw(
        'sdp2025'.encode('utf-8'),
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
        logger.info('User root was created with id=%s.', user_root.id)
    except IntegrityError:
        logger.warning('User root already exists.')
    except AssertionError as e:
        logger.critical('Fatal error. User root was not created: %s', e)
        raise
    finally:
        await sess.aclose()


if __name__ == '__main__':
    asyncio.run(create_root())
