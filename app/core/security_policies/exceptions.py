from dataclasses import dataclass
from typing import final

from fastapi import HTTPException
from starlette import status

from core.enums import TokenTypes
from core.exceptions.base import ApplicationError


class InvalidUsernameOrPasswordError(ApplicationError):
    ...


class InactiveUserError(ApplicationError):
    ...



def get_invalid_type_jwt_exception(
    current_token: TokenTypes = '',
    expected_token: TokenTypes = '',
) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f'invalid token type: {str(current_token)!r}, expected {str(expected_token)!r}',
    )
