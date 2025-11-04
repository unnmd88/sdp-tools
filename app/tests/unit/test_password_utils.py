import pytest

from auth.utils import hash_password

from contextlib import nullcontext


class TestPasswordUtils:

    @pytest.mark.parametrize(
        ('password', 'expected'),
        [
            ('pass1', nullcontext()),
            ('d;asmas', nullcontext()),
            ('osdnf', nullcontext()),
            (1, pytest.raises(AttributeError)),
            ([1, 2, 3], pytest.raises(AttributeError)),
            (list('1234fbi'), pytest.raises(AttributeError))
        ]
    )
    def test_hash_password(self, password, expected):
        with expected:
            # assert isinstance(password, str)
            assert isinstance(hash_password(password), bytes)