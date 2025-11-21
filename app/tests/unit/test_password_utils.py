import random
import string
from contextlib import nullcontext

import pytest
from auth.utils import gen_password, hash_password, validate_password


class TestPasswordUtils:
    @pytest.fixture
    def passwords(self) -> list[str]:
        return [gen_password() for _ in range(4)]

    def test_gen_password(self):
        for passwd_length in range(10, 21):
            _passwd = gen_password(min_length=passwd_length, max_length=passwd_length)
            assert passwd_length == len(_passwd) and isinstance(_passwd, str)

    @pytest.mark.parametrize(
        ('password', 'expected'),
        [
            ('pass1', nullcontext()),
            ('d;asmas', nullcontext()),
            ('osdnf', nullcontext()),
            (1, pytest.raises(AttributeError)),
            ([1, 2, 3], pytest.raises(AttributeError)),
            (list('1234fbi'), pytest.raises(AttributeError)),
        ],
    )
    def test_hash_password(self, password, expected):
        with expected:
            # assert isinstance(password, str)
            assert isinstance(hash_password(password), bytes)

    def test_validate_password_true(self, passwords):
        for passwd in passwords:
            hashed_passwd = hash_password(passwd)
            assert validate_password(passwd, hashed_passwd)

    def test_validate_password_false(self, passwords):
        chars = string.ascii_letters + string.digits + string.punctuation
        for passwd in passwords:
            hashed_passwd = hash_password(passwd)
            chars_added_to_passwd = ''.join(
                random.choices(chars, k=random.randint(1, 10))
            )
            mut_passwd = passwd + chars_added_to_passwd
            assert not validate_password(mut_passwd, hashed_passwd)
