import random

import pytest

from core.enums.entity import EntityIdRange
from core.enums.organizations import Organizations
from core.enums.roles import Roles
from core.users.entities.user import UserEntity
from core.users.exceptions import DomainValidationException
from tests.utils.create_user_entity import create_user_entity

from contextlib import nullcontext


class TestUserEntity:

    def test_create_user_entity_success(self):
        """ Тест на успешное создание сущности UserEntity"""

        _id = random.randint(EntityIdRange.MIN_ID, EntityIdRange.MAX_ID)

        user = UserEntity(
            id=_id,
            first_name='Chook',
            last_name='Gekk',
            username='chokky',
            organization=Organizations.SDP,
            email='example@example.com',
            password=b'mysecret',
            is_active=True,
            is_admin=True,
            is_superuser=True,
            role=Roles.superuser,
            phone_number='',
            telegram='',
            description='',
        )

        assert user.id == _id
        assert user.first_name == "Chook"
        assert user.last_name == "Gekk"
        assert user.username == "chokky"
        assert user.organization == Organizations.SDP
        assert user.email == 'example@example.com'
        assert user.password == b'mysecret'
        assert user.is_active is True
        assert user.is_admin is True
        assert user.is_superuser is True
        assert user.role == Roles.superuser
        assert user.phone_number == ''
        assert user.telegram == ''
        assert user.description == ''

    @pytest.mark.parametrize(
        "bad_id,expectation",
        [
            ('3', pytest.raises(TypeError)),
            (random.uniform(1.0, 32_000.0), pytest.raises(TypeError)),
            (0, pytest.raises(DomainValidationException)),
            (-random.randint(EntityIdRange.MIN_ID, EntityIdRange.MAX_ID), pytest.raises(DomainValidationException)),
            (32001, pytest.raises(DomainValidationException)),
            (123456789, pytest.raises(DomainValidationException)),
        ],
    )
    def test_create_user_entity_exception_bad_id(self, bad_id, expectation):
        """ Тест на вызов ошибки при создании сущности UserEntity с невалидными значениями id. """
        with expectation:
            create_user_entity(_id=bad_id)

    @pytest.mark.parametrize(
        "bad_email,expectation",
        [
            (list(('abra', 'cadabra', 1)), pytest.raises(TypeError)),
            (random.randint(1, 100000000), pytest.raises(TypeError)),
            ('@example.com', pytest.raises(DomainValidationException)),
            ('@', pytest.raises(DomainValidationException)),
            ('12e1e12', pytest.raises(DomainValidationException)),
        ],
    )
    def test_create_user_entity_exception_bad_email(self, bad_email, expectation):
        """ Тест на вызов ошибки при создании сущности UserEntity с невалидными значениями email. """
        with expectation:
            create_user_entity(email=bad_email)

        # for bad_id in ('1', 32001, 123456789, -random.randint(EntityIdRange.MIN_ID, EntityIdRange.MAX_ID)):
        #     with pytest.raises(DomainValidationException):
        #         create_user_entity(_id=bad_id)

        # for bad_mail in ('@example.com', '@', '12e1e12', ):
        #     with pytest.raises(DomainValidationException):
        #         create_user_entity(email=bad_mail)
        #
        # for bad_id in (0, 32001, 123456789, -random.randint(EntityIdRange.MIN_ID, EntityIdRange.MAX_ID)):
        #     with pytest.raises(DomainValidationException):
        #         create_user_entity(_id=bad_id)