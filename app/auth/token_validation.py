from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import InvalidTokenError, ExpiredSignatureError

from auth.constants import TokenTypes
from auth.exceptions import InvalidErrorJWT, ExpiredSignatureJWT, get_invalid_type_jwt_exception
from auth.utils import decode_jwt


http_bearer = HTTPBearer()


def extract_payload_from_jwt(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
) -> dict:
    try:
        payload = decode_jwt(credentials.credentials)
    except ExpiredSignatureError:
        raise ExpiredSignatureJWT
    except InvalidTokenError:
        raise InvalidErrorJWT
    return payload


def check_token_type(
    token_type: TokenTypes,
    expected_type: TokenTypes
) -> bool:
    if token_type != expected_type:
        raise get_invalid_type_jwt_exception(token_type, expected_type)
    return True