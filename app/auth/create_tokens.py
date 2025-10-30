from datetime import timedelta as td

from core.config import settings
from users.schemas import UserFromDbFullSchema

from auth.constants import TokenFields, TokenTypes
from auth.schemas import UserSchema
from auth.utils import encode_jwt


def create_token(
    token_type: TokenTypes,
    payload: dict[str, str],
    expire_minutes: int = settings.auth_jwt.access_expire_minutes,
    expire_timedelta: td | None = None,
):
    return encode_jwt(
        payload=payload | {str(TokenFields.typ): token_type},
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


def create_access_jwt(user: UserSchema | UserFromDbFullSchema):
    payload = {
        str(TokenFields.user_id): user.id,
        str(TokenFields.sub): user.username,
        str(TokenFields.role): user.role,
        str(TokenFields.is_admin): user.is_admin,
        str(TokenFields.is_superuser): user.is_superuser,
        str(TokenFields.organization): user.organization,
        str(TokenFields.email): user.email,
    }
    return create_token(
        token_type=TokenTypes.access,
        payload=payload,
        expire_minutes=settings.auth_jwt.access_expire_minutes,
    )


def create_refresh_jwt(user: UserSchema | UserFromDbFullSchema):
    payload = {
        str(TokenFields.user_id): user.id,
        str(TokenFields.sub): user.username,
    }
    return create_token(
        token_type=TokenTypes.refresh,
        payload=payload,
        expire_timedelta=td(days=settings.auth_jwt.refresh_expire_days),
    )
