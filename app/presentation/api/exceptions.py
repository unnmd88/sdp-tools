from dataclasses import dataclass
from typing import final

from fastapi import HTTPException
from starlette import status

from core.enums import TokenTypes


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






class UserNotFoundHttpException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_404_NOT_FOUND,
        detail: str = None,
    ):
        super().__init__(status_code, detail)


UnauthorizedErrorHttp401 = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid username or password'
)

InactiveUserErrorHttp403 = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail='inactive user'
)


ForbiddenSelfUser = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail='access denied'
)


InvalidErrorJWT = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Invalid token error',
)

ExpiredSignatureJWT = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Signature has expired',
)


