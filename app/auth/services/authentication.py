# from application.interfaces.repositories.users import UsersRepositoryProtocol
# from auth.create_tokens import create_token, create_access_jwt, create_refresh_jwt
# from auth.exceptions import InvalidUsernameOrPasswordException, InactiveUserException
# # from auth.schemas import AuthSchema, TokenInfo
#
#
# class AuthenticationUserServiceImpl:
#     def __init__(
#         self,
#         user_auth_schema: AuthSchema,
#     ):
#         self.user_auth_schema = user_auth_schema
#
#     async def auth_and_issue_jwt(
#         self,
#         refresh_token: bool,
#     ) -> TokenInfo:
#
#         password_is_valid = validate_password(
#             password=self.user_auth_schema.password_plain,
#             hashed_password=self.user_auth_schema.password,
#         )
#         if not password_is_valid:
#             raise InvalidUsernameOrPasswordException
#         if not user.is_active:
#             raise InactiveUserException(user.username)
#         return TokenInfo(
#             access_token=create_access_jwt(user),
#             refresh_token=create_refresh_jwt(user) if refresh_token else None,
#         )
#
#     # async def auth_and_issue_jwt(
#     #     self,
#     #     refresh_token: bool,
#     # ) -> TokenInfo:
#     #     user = await self.repository.get_user_by_username_or_none(
#     #         self.user_auth_schema.username
#     #     )
#     #     if user is None:
#     #         raise InvalidUsernameOrPasswordException
#     #     password_is_valid = validate_password(
#     #         password=self.user_auth_schema.password_plain,
#     #         hashed_password=user.password,
#     #     )
#     #     if not password_is_valid:
#     #         raise InvalidUsernameOrPasswordException
#     #     if not user.is_active:
#     #         raise InactiveUserException(user.username)
#     #     return TokenInfo(
#     #         access_token=create_access_jwt(user),
#     #         refresh_token=create_refresh_jwt(user) if refresh_token else None,
#     #     )
#
#
# # class AuthenticationUserServiceImpl:
# #     def __init__(
# #         self,
# #         user_repository_factory: type[UsersRepositoryProtocol],
# #         user_auth_schema: AuthSchema,
# #     ):
# #         self.repository = user_repository_factory()
# #         self.user_auth_schema = user_auth_schema
# #
# #     async def auth_and_issue_jwt(
# #         self,
# #         refresh_token: bool,
# #     ) -> TokenInfo:
# #         user = await self.repository.get_user_by_username_or_none(
# #             self.user_auth_schema.username
# #         )
# #         if user is None:
# #             raise InvalidUsernameOrPasswordException
# #         password_is_valid = validate_password(
# #             password=self.user_auth_schema.password_plain,
# #             hashed_password=user.password,
# #         )
# #         if not password_is_valid:
# #             raise InvalidUsernameOrPasswordException
# #         if not user.is_active:
# #             raise InactiveUserException(user.username)
# #         return TokenInfo(
# #             access_token=create_access_jwt(user),
# #             refresh_token=create_refresh_jwt(user) if refresh_token else None,
# #         )
