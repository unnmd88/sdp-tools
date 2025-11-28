from fastapi import HTTPException
from starlette import status


class UserNotFoundHttpException(HTTPException):
    def __init__(
            self,
            status_code: int = status.HTTP_404_NOT_FOUND,
            detail: str = None,
    ):
        super().__init__(
            status_code,
            detail
        )

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