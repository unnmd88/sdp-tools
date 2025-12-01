import random
from collections.abc import Sequence

from core.enums import PassportGroups, ServiceOrganizations
from core.models import Passport, PassportGroup, Region, TrafficLightObject, User
from core.users import Organizations
from core.users import Roles


def users_models():
    return [
        User(
            first_name=f'ChoookNoGekk{i}',
            last_name='Choookoffff',
            username=f'Choook{i}',
            organization=Organizations.SDP,
            email='user@example.com',
            password=b'1234',
            is_active=True,
            is_admin=True,
            is_superuser=True,
            role=Roles.superuser,
            phone_number='',
            telegram='',
            description=f'Тестовый юзер {i}',
        )
        for i in range(1, 5)
    ]


def regions_models():
    return [
        Region(code=77, name='Москва'),
        Region(code=78, name='Питер'),
        Region(code=69, name='Тверь'),
        Region(code=65, name='Сахалин'),
    ]


def traffic_light_objects() -> Sequence[TrafficLightObject]:
    return [
        TrafficLightObject(
            region_id=1,
            name=f'BazaBereg{i}',
            district='ЦАО',
            street='Бережковская набережная',
            service_organization=ServiceOrganizations.CODD,
            description=f'Тестовый_00{i}',
        )
        for i in range(1, 5)
    ]


def passports_owners_models():
    return [
        PassportGroup(owner=PassportGroups.OVIM),
        PassportGroup(owner=PassportGroups.STROYKONTROL),
    ]


def passports_models():
    datas = [{}] + [
        {
            f'Field_{i}': i if i % 2 == 0 else str(i)
            for i in range(random.randint(1, 10))
        }
        for _ in range(1, 4)
    ]
    return [
        Passport(
            tlo_id=random.randint(1, 4),
            data=datas[i - 1],
            user_id=1,
            owner_id=random.randint(1, 2),
            commit_message=f'commit_message{i}',
        )
        for i in range(1, 5)
    ]
