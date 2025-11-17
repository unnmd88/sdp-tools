from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from auth.schemas import PayloadJWTSchema
from auth.utils import decode_jwt

http_bearer = HTTPBearer()


def get_jwt_payload_jwt_bearer(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)]
):
    return PayloadJWTSchema(**decode_jwt(credentials.credentials))
