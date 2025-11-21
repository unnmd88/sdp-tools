from contextlib import nullcontext

import pytest
from auth.constants import TokenTypes
from auth.token_validation import check_token_type
from fastapi import HTTPException


@pytest.mark.parametrize(
    ('token_type', 'expected_token_type', 'expected_res'),
    [
        (TokenTypes.access, TokenTypes.access, nullcontext()),
        (TokenTypes.refresh, TokenTypes.refresh, nullcontext()),
        (TokenTypes.access, TokenTypes.refresh, pytest.raises(HTTPException)),
        (TokenTypes.refresh, TokenTypes.access, pytest.raises(HTTPException)),
    ],
)
def test_check_token_type(token_type, expected_token_type, expected_res):
    with expected_res:
        assert check_token_type(token_type, expected_token_type)
