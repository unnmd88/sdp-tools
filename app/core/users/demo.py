# from enum import StrEnum
# from typing import Annotated
#
# from auth import utils as auth_utils
# from core.models import db_api
# from fastapi import APIRouter, Depends, Form, HTTPException, status
# from pydantic import BaseModel
# from sqlalchemy.ext.asyncio.session import AsyncSession
#
# from users.schemas import UserSchema
#
# # router = APIRouter(prefix='/jwt', tags=['JWT'])
#
# session = Annotated[
#     AsyncSession,
#     Depends(db_api.session_getter),
# ]
#
#
# class TokenFields(StrEnum):
#     access = 'access'
#     bearer = 'Bearer'
#     username = 'username'
#     sub = 'sub'
#     exp = 'exp'
#     pk_id = 'id'
#     email = 'email'
#
#
# class TokenInfo(BaseModel):
#     access_token: str
#     token_type: str
#
#
# def validate_auth_user(
#     username: str = Form(),
#     password: str = Form(),
# ):
#     unauthed_exc = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid username or password'
#     )
#     if not (user := demo_db.get(username)):
#         raise unauthed_exc
#     if not auth_utils.validate_password(
#         password=password, hashed_password=user.password
#     ):
#         raise unauthed_exc
#     if not user.is_active:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, detail='inactive user'
#         )
#     return user
#
#
# @router.post('/login/')
# def auth_user_issue_jwt(user: UserSchema = Depends(validate_auth_user)):
#     jwt_payload = {
#         str(TokenFields.sub): user.id,
#         str(TokenFields.username): user.username,
#         str(TokenFields.email): user.email,
#     }
#     token = auth_utils.encode_jwt(jwt_payload)
#     return TokenInfo(
#         access_token=token,
#         token_type=str(TokenFields.bearer),
#     )
#
#
# # @router.post('/create/')
# # async def auth_user_issue_jwt(
# #         user: CreateUser,
# #         sess: session,
# # ):
# #     user.password = hash_password(user.password)
# #     new_user = User(**user.model_dump())
# #     sess.add(new_user)
# #     await sess.commit()
# #     res = await sess.execute(text("SELECT * FROM users"))
# #     print(res)
# #     return user
