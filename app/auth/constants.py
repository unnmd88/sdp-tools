from enum import StrEnum


class TokenFields(StrEnum):
    pk_id = 'id'
    user_id = 'user_id'
    username = 'username'
    sub = 'sub'
    exp = 'exp'
    email = 'email'
    role = 'role'
    iat = 'iat'
    is_admin = 'is_admin'
    is_active = 'is_active'
    is_superuser = 'is_superuser'
    organization = 'organization'
    typ = 'typ'


class TokenTypes(StrEnum):
    access = 'access'
    refresh = 'refresh'