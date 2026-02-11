from domain.kernel.enums import PassportGroups
from domain.passports.entities.passport import PassportEntity
import pytest

from tests.utils.create_user_entity import create_user_entity


class TestPassportEntity:
    @pytest.mark.parametrize(
        "data,user,group",
        [
            (dict(), create_user_entity(username="chook"), PassportGroups.OVIM),
            (
                dict(data={}),
                create_user_entity(username="gekk"),
                PassportGroups.STROYKONTROL,
            ),
            (
                dict(data=dict(nested=dict())),
                create_user_entity(username="chookAndGekk"),
                PassportGroups.CODD,
            ),
        ],
    )
    def test_create_passport_entities_success(self, data, user, group):
        """Тест на успешное создание value-object Passport."""
        PassportEntity(
            data=data, username=user, group=group, commit_message="test commit message"
        )
