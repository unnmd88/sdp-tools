from collections.abc import MutableMapping
from enum import StrEnum

from fastapi import APIRouter, Depends, Form, HTTPException, status

from users.schemas import UserSchema

from auth import utils as auth_utils

from pydantic import BaseModel

router = APIRouter(prefix='/jwt', tags=["JWT"])


class TokenFields(StrEnum):
    access = 'access'
    bearer = 'Bearer'
    username = 'username'
    sub = 'sub'
    exp = 'exp'
    pk_id = 'id'
    email = 'email'


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


pimmo = UserSchema(
    id=1,
    username='Pimmo',
    password=auth_utils.hash_password('1234'),
    is_active=True,
    is_admin=True
)
nyanya = UserSchema(
    id=2,
    username='Nyanya',
    password=auth_utils.hash_password('3456'),
    is_active=True,
)

demo_db: MutableMapping[str, UserSchema] = {
    pimmo.username: pimmo,
    nyanya.username: nyanya
}

def validate_auth_user(username: str = Form(), password: str = Form(),):
    unauthed_exc =  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid username or password')
    if not (user := demo_db.get(username)):
        raise unauthed_exc
    if not auth_utils.validate_password(password=password, hashed_password=user.password):
        raise unauthed_exc
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='inactive user')
    return user


@router.post('/login/')
def auth_user_issue_jwt(
        user: UserSchema = Depends(validate_auth_user)
):
    jwt_payload = {
        str(TokenFields.sub): user.id,
        str(TokenFields.username): user.username,
        str(TokenFields.email): user.email,
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type=str(TokenFields.bearer),
    )
print(auth_utils.hash_password('1234'))