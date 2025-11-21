from typing import Annotated

from auth.schemas import PayloadJWTSchema
from auth.utils import decode_jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

http_bearer = HTTPBearer()


def get_jwt_payload_jwt_bearer(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
):
    return PayloadJWTSchema(**decode_jwt(credentials.credentials))
