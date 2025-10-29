from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth import utils as auth_utils
from auth.services import validate_auth_user
from auth.constants import TokenFields
from auth.schemas import TokenInfo
from core.models import db_api
from auth.schemas import UserSchema

router = APIRouter(prefix="/auth", tags=["Auth"])


db_session = Annotated[
    AsyncSession,
    Depends(db_api.session_getter),
]


@router.post('/login/')
async def auth_user_issue_jwt(user: UserSchema = Depends(validate_auth_user)):
    print('-------LOGIN JWT--------')
    print(user)

    jwt_payload = {
        str(TokenFields.sub): user.id,
        str(TokenFields.username): user.username,
        str(TokenFields.role): user.role,
        str(TokenFields.is_admin): user.is_admin,
        str(TokenFields.is_superuser): user.is_superuser,
        str(TokenFields.organization): user.organization,
        str(TokenFields.email): user.email,
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
    )