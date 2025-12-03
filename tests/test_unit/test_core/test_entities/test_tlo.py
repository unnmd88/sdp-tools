import datetime


from core.enums import RegionNames, ServiceOrganizations, PassportGroups
from core.tlo.entities.tlo import TrafficLightObjectEntity
from core.tlo.value_objects.passport import Passport
from tests.utils.create_user_entity import create_user_entity


class TestTrafficLightObjectEntity:

    def test_create_tlo_entity_success(self, pk_id):
        """ Тест на успешное создание сущности TrafficLightObjectEntity. """

        user = create_user_entity(username='chook')

        passport = Passport(
            data={"data": {}},
            created_by=user,
            group=PassportGroups.OVIM,
            commit_message='test commit message'
        )

        tlo = TrafficLightObjectEntity(
            id=pk_id,
            region=RegionNames.MOSCOW,
            name='413',
            district='ЦАО',
            street='Площадь Тверской заставы',
            service_organization=ServiceOrganizations.CODD,
            description='Тестовый объект',
            editing_now=False,
            current_passport=passport,
            passport_history=[],
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )
        assert tlo.id == pk_id
        assert tlo.region == RegionNames.MOSCOW
        assert tlo.name == '413'
        assert tlo.district == 'ЦАО'
        assert tlo.street == 'Площадь Тверской заставы'
        assert tlo.service_organization == ServiceOrganizations.CODD
        assert tlo.description == 'Тестовый объект'
        assert tlo.editing_now == False
        assert tlo.current_passport == passport
        assert tlo.current_passport.created_by == user
        assert tlo.passport_history == []
        assert isinstance(tlo.created_at, datetime.datetime)
        assert isinstance(tlo.updated_at, datetime.datetime)

