from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from auth.schemas import PayloadJWTSchema
from auth.utils import decode_jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from infra.database.api import db_api

http_bearer = HTTPBearer()


db_session = Annotated[
    AsyncSession,
    Depends(db_api.session_getter),
]


def get_jwt_payload_jwt_bearer(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
):
    return PayloadJWTSchema(**decode_jwt(credentials.credentials))
