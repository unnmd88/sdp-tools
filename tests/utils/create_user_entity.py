import random

from core.enums.entity import EntityIdRange
from core.enums.organizations import Organizations
from core.enums.roles import Roles
from core.users.entities.user import UserEntity


def create_user_entity(
        _id=random.randint(EntityIdRange.MIN_ID, EntityIdRange.MAX_ID),
        first_name='Chook',
        last_name='Gekk',
        username='chokky',
        organization=Organizations.SDP,
        email='good_mail@mail.com',
        password=b'good_password',
        is_active=True,
        is_admin=True,
        is_superuser=True,
        role=Roles.superuser,
        phone_number='',
        telegram='',
        description='',
) -> UserEntity:
    return UserEntity(
            id=_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            organization=organization,
            email=email,
            password=password,
            is_active=is_active,
            is_admin=is_admin,
            is_superuser=is_superuser,
            role=role,
            phone_number=phone_number,
            telegram=telegram,
            description=description,
        )