import asyncio

from core.constants import (
    PassportGroups,
    PassportGroupsRoutes,
    RegionCodes,
    RegionNames,
    ServiceOrganizations,
)
from core.database import db_api
from core.models import PassportGroup, Region, TrafficLightObject
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import select

REGIONS = [
    Region(code=RegionCodes.MOSCOW77, name=RegionNames.MOSCOW),
    Region(code=RegionCodes.TVER69, name=RegionNames.TVER),
    Region(code=RegionCodes.RYBINSK76, name=RegionNames.RYBINSK),
]

PASSPORT_GROUPS = [
    PassportGroup(
        group_name=PassportGroups.OVIM,
        group_name_route=PassportGroupsRoutes.OVIM,
    ),
    PassportGroup(
        group_name=PassportGroups.STROYKONTROL,
        group_name_route=PassportGroupsRoutes.STROYKONTROL,
    ),
    PassportGroup(
        group_name=PassportGroups.CODD,
        group_name_route=PassportGroupsRoutes.CODD,
    ),
]
TLO_DATA = [
    ('413', ServiceOrganizations.CODD),
    ('155', ServiceOrganizations.CODD),
    ('11', ServiceOrganizations.CODD),
    ('510', ServiceOrganizations.CODD),
    ('!TEST', ServiceOrganizations.CODD),
    ('!!TEST', ServiceOrganizations.CODD),
]


async def add_tlo(session: AsyncSession):
    stmt = select(Region).filter_by(code=RegionCodes.MOSCOW77)
    res = await session.execute(stmt)
    pk_region77 = res.scalars().one().id
    for name, service_organization in TLO_DATA:
        session.add(
            TrafficLightObject(
                region_id=pk_region77,
                name=name,
                service_organization=service_organization.CODD,
                district='',
                street='',
                description='',
            )
        )
    try:
        await session.commit()
    except IntegrityError as e:
        print(f'IntegrityError. Add tlo Failed: {e}.')
        await session.rollback()
    except Exception as e:
        print(f'Add tlo Failed: {e}.')
        await session.rollback()


async def add_regions_and_passport_groups(session: AsyncSession):
    try:
        session.add_all(REGIONS)
        session.add_all(PASSPORT_GROUPS)
        await session.commit()
    except IntegrityError:
        print('Failed: already exists.')
        await session.rollback()


async def main():
    async with db_api.session_factory() as session:
        await add_regions_and_passport_groups(session)
        await add_tlo(session)


if __name__ == '__main__':
    asyncio.run(main())
