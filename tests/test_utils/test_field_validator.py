from contextlib import nullcontext

import pytest

from core.utils import checking_simple_types


@pytest.mark.parametrize(
    'type_to_check,value,expectation',
    [   #Ok section
        (int, 1, nullcontext()),
        (str, 'some_text', nullcontext()),
        (list, list(), nullcontext()),
        (tuple, tuple(), nullcontext()),
        (dict, dict(), nullcontext()),
        (set, set(), nullcontext()),
        # Raise if not int section
        (int, '1', pytest.raises(TypeError)),
        (int, ['1'], pytest.raises(TypeError)),
        (int, (1, 2, 3), pytest.raises(TypeError)),
        (int, {'1': 1}, pytest.raises(TypeError)),
        (int, {1}, pytest.raises(TypeError)),
        (int, None, pytest.raises(TypeError)),
        # Raise if not str section
        (str, (), pytest.raises(TypeError)),
        (str, 1, pytest.raises(TypeError)),
        (str, ['1'], pytest.raises(TypeError)),
        (str, (1, 2, 3), pytest.raises(TypeError)),
        (str, {'1': 1}, pytest.raises(TypeError)),
        (str, {1}, pytest.raises(TypeError)),
        (str, None, pytest.raises(TypeError)),
        # Raise if tuple section
        (tuple, '1', pytest.raises(TypeError)),
        (tuple, 1, pytest.raises(TypeError)),
        (tuple, ['1'], pytest.raises(TypeError)),
        (tuple, {'1': 1}, pytest.raises(TypeError)),
        (tuple, {1}, pytest.raises(TypeError)),
        (tuple, None, pytest.raises(TypeError)),
        # Raise if not list section
        (list, tuple(), pytest.raises(TypeError)),
        (list, '1', pytest.raises(TypeError)),
        (list, 1, pytest.raises(TypeError)),
        (list, {'1': 1}, pytest.raises(TypeError)),
        (list, {1}, pytest.raises(TypeError)),
        (list, None, pytest.raises(TypeError)),
        # Raise if not dict section
        (dict, tuple(), pytest.raises(TypeError)),
        (dict, '1', pytest.raises(TypeError)),
        (dict, 1, pytest.raises(TypeError)),
        (dict, list(), pytest.raises(TypeError)),
        (dict, set(), pytest.raises(TypeError)),
        (dict, None, pytest.raises(TypeError)),
        # Raise if not set section
        (set, tuple(), pytest.raises(TypeError)),
        (set, '1', pytest.raises(TypeError)),
        (set, 1, pytest.raises(TypeError)),
        (set, list(), pytest.raises(TypeError)),
        (set, dict(), pytest.raises(TypeError)),
        (set, None, pytest.raises(TypeError)),
    ]
)
def test_type_validator(type_to_check, value, expectation):
    with expectation:
        @checking_simple_types(type_to_check=type_to_check)
        def stub(v):
            return v
        stub(value)
