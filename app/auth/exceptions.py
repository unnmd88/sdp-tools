from dataclasses import dataclass
from typing import final

from fastapi import HTTPException
from starlette import status

from core.enums.tokens import TokenTypes


class BaseAuthException(Exception):
    pass


@final
@dataclass
class InvalidUsernameOrPasswordException(BaseAuthException):
    @property
    def detail(self) -> str:
        return 'invalid username or password'


@final
@dataclass
class InactiveUserException(BaseAuthException):
    user: str | int = ''

    @property
    def detail(self) -> str:
        return f'User {self.user!r} is inactive'.replace('  ', ' ')


def get_invalid_type_jwt_exception(
    current_token: TokenTypes = '',
    expected_token: TokenTypes = '',
) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f'invalid token type: {str(current_token)!r}, expected {str(expected_token)!r}',
    )
