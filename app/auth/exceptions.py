from fastapi import HTTPException
from starlette import status

from auth.constants import TokenTypes

AuthenticationError = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid username or password'
)

InactiveUserError = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail='inactive user'
)

InvalidErrorJWT = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Invalid token error',
)

ExpiredSignatureJWT = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Signature has expired',
)


def get_invalid_type_jwt_exception(
    current_token: TokenTypes = '',
    expected_token: TokenTypes = '',
) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid token type: {str(current_token)!r}, expected {str(expected_token)!r}",
    )