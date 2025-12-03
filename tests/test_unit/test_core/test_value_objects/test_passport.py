from core.enums import PassportGroups
from core.tlo.value_objects.passport import Passport
import pytest

from tests.utils.create_user_entity import create_user_entity


class TestPassportValueObject:

    @pytest.mark.parametrize(
        "data,user,group",
        [
            (dict(), create_user_entity(username='chook'), PassportGroups.OVIM),
            (dict(data={}),create_user_entity(username='gekk'), PassportGroups.STROYKONTROL),
            (dict(data=dict(nested=dict())), create_user_entity(username='chookAndGekk'), PassportGroups.CODD),
        ],
    )
    def test_create_passport_value_object_success(self, data, user, group):
        """ Тест на успешное создание value-object Passport. """
        Passport(
            data=data,
            created_by=user,
            group=group,
            commit_message='test commit message'
        )


