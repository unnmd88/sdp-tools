from contextlib import nullcontext
from enum import StrEnum, IntEnum

import pytest

from core.utils import type_validator


class StrEnumForTest(StrEnum):
    some_text1 = 'some_text1'
    some_text2 = 'some_text2'


class IntEnumForTest(IntEnum):
    NUM1 = 1
    NUM2 = 2


@pytest.mark.parametrize(
    'type_to_check,value,expectation',
    [
        (int, 1, nullcontext()),
        (StrEnumForTest, 'some_text1', nullcontext()),
        (StrEnumForTest, 'some_text2', nullcontext()),
        (IntEnumForTest, 1, nullcontext()),
        (IntEnumForTest, 2, nullcontext()),
        (int, '1', pytest.raises(TypeError)),
        (StrEnumForTest, 1, pytest.raises(TypeError)),
        (StrEnumForTest, 1234, pytest.raises(TypeError)),
        (IntEnumForTest, '1234', pytest.raises(TypeError)),
        (StrEnumForTest, '1', pytest.raises(TypeError)),
    ]
)
def test_type_validator(type_to_check, value, expectation):
    with expectation:
        @type_validator(type_to_check=type_to_check)
        def stub(v):
            return v
        stub(value)
