from enum import StrEnum


class TokenFields(StrEnum):
    pk_id = 'id'
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