from core.enums import PassportGroups
from core.tlo.value_objects.passport import Passport
import pytest


class TestPassportValueObject:

    @pytest.mark.parametrize(
        "data,created_by,group",
        [
            (dict(), 'chook', PassportGroups.OVIM),
            (dict(data={}), 'gekk', PassportGroups.STROYKONTROL),
            (dict(data=dict(nested=dict())), 'chook', PassportGroups.CODD),
        ],
    )
    def test_create_passport_value_object_success(self, data, created_by, group):
        """ Тест на успешное создание value-object Passport. """
        Passport(
            data=data,
            created_by=created_by,
            group=group,
            commit_message='test commit message'
        )


