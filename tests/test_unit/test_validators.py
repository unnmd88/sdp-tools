import random

import pytest

from core.enums import EntityIdRange
from core.field_validators import (
    check_field_id_is_valid,
    check_email_is_valid, check_firstname_is_valid, check_lastname_is_valid, check_username_is_valid,
    check_password_is_valid, check_phone_number_is_valid
)


class TestValidators:

    @pytest.mark.parametrize(
        '_id,expected',
        [
            (random.randint(EntityIdRange.MIN_ID, EntityIdRange.MAX_ID), True),
            (random.randint(EntityIdRange.MIN_ID, EntityIdRange.MAX_ID), True),
            (0, False),
            (3412414214, False),
            (-random.randint(EntityIdRange.MIN_ID, 9126731924872154), False),
        ]
    )
    def test_check_field_id_is_valid(self, _id, expected):
        """ Тест валидности id для объекта домена. """
        assert check_field_id_is_valid(_id) == expected

    @pytest.mark.parametrize(
        'firstname,expected',
        [
            ('Chook', True),
            ('', True),
        ]
    )
    def test_check_firstname_is_valid(self, firstname, expected):
        """ Тест валидности firstname для объекта домена. """
        assert check_firstname_is_valid(firstname) == expected

    @pytest.mark.parametrize(
        'lastname,expected',
        [
            ('Gekk', True),
            ('', True),
        ]
    )
    def test_check_lastname_is_valid(self, lastname, expected):
        """ Тест валидности lastname для объекта домена. """
        assert check_lastname_is_valid(lastname) == expected

    @pytest.mark.parametrize(
        'username,expected',
        [
            ('Gekk', True),
            ('Gaga', True),
            ('Simple_User', True),
            ('Simpleuser', True),
            ('Simpleuser1234', True),
            ('Simpleuser_1234', True),
            ('G', False),
            ('', False),
        ]
    )
    def test_check_username_is_valid(self, username, expected):
        """ Тест валидности username для объекта домена. """
        assert check_username_is_valid(username) == expected

    @pytest.mark.parametrize(
        'email,expected',
        [
            ('simple@mail.com', True),
            ('john_doe@example.io', True),
            ('john_doe', False),
            ('@', False),
            ('com', False),
        ]
    )
    def test_check_email_is_valid(self, email, expected):
        """ Тест валидности email для объекта домена. """
        assert check_email_is_valid(email) == expected

    @pytest.mark.parametrize(
        'password,expected',
        [
            (b'MF@0fh203fnfbf2@hF93', True),
            (b'MF@0fh2fsdfsfbcxxcxmvcmfnfbf2@hF93', True),
            (b'j', False),
            (b'', False),
        ]
    )
    def test_check_password_is_valid(self, password, expected):
        """ Тест валидности password для объекта домена. """
        assert check_password_is_valid(password) == expected

    @pytest.mark.parametrize(
        'phone_number,expected',
        [
            ('', True),
            ('1112223344', True),
            ('1234567890', True),
            ('9998887766', True),
            ('1', False),
            ('2', False),
            ('dasee', False),
            ('12342134234', False),
            ('fasfa33f3', False),
        ]
    )
    def test_check_phone_number_is_valid(self, phone_number, expected):
        """ Тест валидности phone_number для объекта домена. """
        assert check_phone_number_is_valid(phone_number) == expected