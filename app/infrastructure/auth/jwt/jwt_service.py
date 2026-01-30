import datetime
import logging
from datetime import datetime as dt, timedelta as td
from functools import lru_cache
from pathlib import Path
from typing import AnyStr

import jwt

from app_logging.dev.config import INFRASTRUCTURE
from application.dto.jwt_dto import AccessJWTPayloadDTO, RefreshJWTPayloadDTO, TokenDataDTO, PayloadJWTDTO
from application.dto.users import UserDTO
from domain.enums.validation_err_messages import ErrorMessages
from domain.value_objects.token_error_context_vo import TokenErrorContextVO
from infrastructure.auth.exceptions import  RottenTokenError
from domain.enums.unsorted import TokenTypesEnum, Organizations, Roles
from infrastructure.exceptions import TokenError, InvalidTokenTypeError

logger = logging.getLogger(INFRASTRUCTURE)


# class JWTService:
#
#     def __init__(
#         self,
#         *,
#         expire_minutes_access_token: int,
#         expire_days_refresh_token: int,
#         public_key: Path | str,
#         private_key: Path | str,
#         algorithm: str,
#     ):
#         self._public_key = self._load_key(public_key)
#         self._private_key = self._load_key(private_key)
#         self._expire_minutes_access_token = expire_minutes_access_token
#         self._expire_days_refresh_token = expire_days_refresh_token
#         self._algorithm = algorithm
#
#     @staticmethod
#     @lru_cache(maxsize=4)
#     def _load_key(key: Path | str) -> str:
#         if isinstance(key, Path):
#             return key.resolve().read_text(encoding="utf-8")
#         return key
#
#     def encode_jwt(
#         self,
#         *,
#         user_dto: UserDTO,
#         token_type: TokenTypesEnum,
#     ) -> str:
#         now = dt.now(datetime.UTC)
#         if token_type == TokenTypesEnum.access:
#             payload = AccessJWTPayloadDTO(
#                 user_id=user_dto.id,
#                 sub=user_dto.username,
#                 role=user_dto.role,
#                 organization=user_dto.organization,
#                 email=user_dto.email,
#                 iat=now,
#                 exp=now + td(minutes=self._expire_minutes_access_token),
#                 typ=token_type,
#             )
#         elif token_type == TokenTypesEnum.refresh:
#             payload = RefreshJWTPayloadDTO(
#                 user_id=user_dto.id,
#                 sub=user_dto.username,
#                 iat=now,
#                 exp=now + td(days=self._expire_days_refresh_token),
#                 typ=token_type,
#             )
#         else:
#             ctx = TokenErrorContextVO(
#                 token_type=token_type,
#                 subject=self.__class__.__name__,
#                 handler=self.encode_jwt.__name__,
#                 internal_message=ErrorMessages.unknown_token_type.format(token_type),
#                 message=ErrorMessages.invalid_token_type.format(token_type),
#             )
#             exc = TokenError(
#                 context=ctx,
#                 message=ctx.message,
#             )
#             logger.warning(exc.to_dict())
#             raise exc
#         try:
#             return jwt.encode(
#                 payload=payload.to_dict(),
#                 key=self._private_key,
#                 algorithm=self._algorithm,
#             )
#         except jwt.exceptions.PyJWTError as e:
#             ctx = TokenErrorContextVO(
#                 token_type=token_type,
#                 subject=self.__class__.__name__,
#                 handler=self.encode_jwt.__name__,
#                 internal_message=str(e),
#             )
#             exc = TokenError(
#                 context=ctx,
#                 message=ctx.message,
#             )
#             logger.error(exc.to_dict())
#             raise exc
#
#     def decode_jwt(self, token: AnyStr) -> AccessJWTPayloadDTO | RefreshJWTPayloadDTO:
#         try:
#             decoded_jwt = jwt.decode(
#                 jwt=token,
#                 key=self._public_key,
#                 algorithms=[self._algorithm],
#             )
#         except jwt.ExpiredSignatureError:
#             raise RottenTokenError
#         except jwt.PyJWTError as e:
#             ctx = TokenErrorContextVO(
#                 token=token,
#                 subject=self.__class__.__name__,
#                 handler=self.decode_jwt.__name__,
#                 internal_message=str(e),
#             )
#             exc = TokenError(context=ctx)
#             logger.error(exc.to_dict())
#             raise exc
#         try:
#             token_type = decoded_jwt["typ"]
#         except KeyError:
#             ctx = TokenErrorContextVO(
#                 token=token,
#                 subject=self.__class__.__name__,
#                 handler=self.decode_jwt.__name__,
#                 internal_message="Не найдено поле 'typ' в токене при декодировании",
#             )
#             exc = TokenError(context=ctx)
#             logger.error(exc.to_dict())
#             raise exc
#         if token_type == TokenTypesEnum.access:
#             dto = AccessJWTPayloadDTO
#         elif token_type == TokenTypesEnum.refresh:
#             dto = RefreshJWTPayloadDTO
#         else:
#             ctx = TokenErrorContextVO(
#                 token=token,
#                 token_type=token_type,
#                 subject=self.__class__.__name__,
#                 handler=self.decode_jwt.__name__,
#                 internal_message=f"Недопустимый тип токена: {token_type!r}",
#             )
#             exc = TokenError(context=ctx)
#             logger.error(exc.to_dict())
#             raise exc
#         return dto(**decoded_jwt)
#
#     def create_access_jwt(self,user_dto: UserDTO) -> str:
#         return self.encode_jwt(
#             user_dto=user_dto,
#             token_type=TokenTypesEnum.access,
#         )
#
#     def create_refresh_jwt(self,user_dto: UserDTO) -> str:
#         return self.encode_jwt(
#             user_dto=user_dto,
#             token_type=TokenTypesEnum.refresh,
#         )
#
#     def issue_access_jwt(self, user_dto: UserDTO) -> TokenDataDTO:
#         return TokenDataDTO(
#             access_token=self.create_access_jwt(user_dto=user_dto ),
#             refresh_token=None,
#         )
#
#     def issue_pair(self, user_dto: UserDTO) -> TokenDataDTO:
#         return TokenDataDTO(
#             access_token=self.create_access_jwt(user_dto=user_dto),
#             refresh_token=self.create_refresh_jwt(user_dto=user_dto),
#         )
#
#     def verify_token(self, token: str) -> bool:
#         """Проверить валидность токена"""
#         try:
#             self.decode_jwt(token)
#             return True
#         except (RottenTokenError, TokenError):
#             return False


class DecodeJWTService:
    def __init__(
        self,
        *,
        public_key: str,
        algorithm: str,
        # expected_type: TokenTypesEnum,
    ):
        self._public_key = public_key
        self._algorithm = algorithm
        # self._expected_type = expected_type


    # @staticmethod
    # @lru_cache(maxsize=4)
    # def _load_key(key: Path | str) -> str:
    #     if isinstance(key, Path):
    #         return key.resolve().read_text(encoding="utf-8")
    #     return key
    
    def _decode_jwt(self, token: str,):
        try:
            return jwt.decode(
                jwt=token,
                key=self._public_key,
                algorithms=[self._algorithm],
            )
        except jwt.ExpiredSignatureError:
            raise RottenTokenError
        except jwt.PyJWTError as e:
            ctx = TokenErrorContextVO(
                token=token,
                subject=self.__class__.__name__,
                handler=self._decode_jwt.__name__,
                internal_message=str(e),
            )
            exc = TokenError(context=ctx)
            logger.error(exc.to_dict())
            raise exc
    
    def _validate_token_type(
        self,
        *,
        raw_token: str,
        decoded_token: dict[str, AnyStr],
        expected_type: TokenTypesEnum,
    ) -> TokenTypesEnum:
        if (current_token_type := decoded_token.get("typ")) is None:
            ctx = TokenErrorContextVO(
                token=raw_token,
                subject=self.__class__.__name__,
                handler=self._validate_token_type.__name__,
                internal_message="Не найдено поле 'typ' в токене при декодировании",
            )
            exc = TokenError(context=ctx)
            logger.critical(exc.to_dict())
            raise exc
        if current_token_type != expected_type:
            ctx = TokenErrorContextVO(
                token=raw_token,
                expected_token_type=expected_type,
                subject=self.__class__.__name__,
                handler=self._validate_token_type.__name__,
                message=ErrorMessages.invalid_token_type.format(expected_type),
            )
            exc = InvalidTokenTypeError(context=ctx)
            logger.warning(exc.to_dict())
        return current_token_type
    
    def decode_and_validate_type_jwt(
        self,
        *,
        token: str,
        expected_type: TokenTypesEnum,
    ) -> AccessJWTPayloadDTO | RefreshJWTPayloadDTO:
        decoded_jwt = self._decode_jwt(token)      
        current_token_type = self._validate_token_type(
            raw_token=token,
            decoded_token=decoded_jwt,
            expected_type=expected_type,
        )
        if current_token_type == TokenTypesEnum.access:
            dto = AccessJWTPayloadDTO
        elif current_token_type == TokenTypesEnum.refresh:
            dto = RefreshJWTPayloadDTO
        else:
            ctx = TokenErrorContextVO(
                token=token,
                token_type=current_token_type,
                subject=self.__class__.__name__,
                handler=self.decode_and_validate_type_jwt.__name__,
                internal_message=f"Недопустимый тип токена: {current_token_type!r}",
            )
            exc = TokenError(context=ctx)
            logger.error(exc.to_dict())
            raise exc
        return dto(**decoded_jwt)
    
    def decode_access_jwt(self, token: str) -> AccessJWTPayloadDTO:
        return self.decode_and_validate_type_jwt(token=token, expected_type=TokenTypesEnum.access)
    
    def decode_refresh_jwt(self, token: str) -> AccessJWTPayloadDTO:
        return self.decode_and_validate_type_jwt(token=token, expected_type=TokenTypesEnum.refresh)
    
    def verify_token(self, token: str) -> bool:
        """Проверить валидность токена"""
        try:
            self.decode_and_validate_type_jwt(token)
            return True
        except (RottenTokenError, TokenError):
            return False


class IssueJWTService:
    def __init__(
        self,
        *,
        expire_minutes_access_token: int,
        expire_days_refresh_token: int,
        private_key: str,
        algorithm: str,
    ):
        self._expire_minutes_access_token = expire_minutes_access_token
        self._expire_days_refresh_token = expire_days_refresh_token
        self._private_key = private_key
        self._algorithm = algorithm

    def _encode_jwt(
        self,
        *,
        payload_dto: PayloadJWTDTO,
        token_type: TokenTypesEnum,
    ) -> str:
        now = dt.now(datetime.UTC)
        if token_type == TokenTypesEnum.access:
            payload = AccessJWTPayloadDTO(
                user_id=payload_dto.user_id,
                sub=payload_dto.sub,
                role=payload_dto.role,
                organization=payload_dto.organization,
                email=payload_dto.email,
                iat=now,
                exp=now + td(minutes=self._expire_minutes_access_token),
                typ=token_type,
            )
        elif token_type == TokenTypesEnum.refresh:
            payload = RefreshJWTPayloadDTO(
                user_id=payload_dto.user_id,
                sub=payload_dto.sub,
                iat=now,
                exp=now + td(days=self._expire_days_refresh_token),
                typ=token_type,
            )
        else:
            ctx = TokenErrorContextVO(
                token_type=token_type,
                subject=self.__class__.__name__,
                handler=self._encode_jwt.__name__,
                internal_message=ErrorMessages.unknown_token_type.format(token_type),
                message=ErrorMessages.invalid_token_type.format(token_type),
            )
            exc = TokenError(
                context=ctx,
                message=ctx.message,
            )
            logger.warning(exc.to_dict())
            raise exc
        try:
            return jwt.encode(
                payload=payload.to_dict(),
                key=self._private_key,
                algorithm=self._algorithm,
            )
        except jwt.exceptions.PyJWTError as e:
            ctx = TokenErrorContextVO(
                token_type=token_type,
                subject=self.__class__.__name__,
                handler=self._encode_jwt.__name__,
                internal_message=str(e),
            )
            exc = TokenError(
                context=ctx,
                message=ctx.message,
            )
            logger.error(exc.to_dict())
            raise exc

    def issue_access_jwt(self, payload_dto: PayloadJWTDTO) -> TokenDataDTO:
        return TokenDataDTO(
            access_token=self._encode_jwt(payload_dto=payload_dto, token_type=TokenTypesEnum.access),
            refresh_token=None,
        )

    def issue_pair(self, payload_dto: PayloadJWTDTO) -> TokenDataDTO:
        return TokenDataDTO(
            access_token=self._encode_jwt(payload_dto=payload_dto, token_type=TokenTypesEnum.access),
            refresh_token=self._encode_jwt(payload_dto=payload_dto, token_type=TokenTypesEnum.refresh),
        )


if __name__ == "__main__":
    _user_dto = UserDTO(
        id=1,
        firstname="Junker",
        lastname="Junker",
        username="test",
        role=Roles.superuser,
        organization=Organizations.SDP,
        email="test@test.com",
        is_superuser=True,
        is_active=True,
        phone_number=None,
        telegram="test_telegram",
        description="test_description",
        created_at=None,
        updated_at=None,
        built_at=datetime.datetime.now(),
    )
    print(_user_dto)

    jwt_service = DecodeJWTService(
        expire_minutes_access_token=expire_rules.expire_minutes_access_token,
        expire_days_refresh_token=expire_rules.expire_days_refresh_token,
        public_key=security_rules.public_key_path,
        private_key=security_rules.private_key_path,
        algorithm=security_rules.algorithm,
    )

    encoded_jwt = jwt_service.create_access_jwt(user_dto=_user_dto)
    print(encoded_jwt)

    decoded_jwt = jwt_service.decode_and_validate_type_jwt(token=encoded_jwt)
    print(decoded_jwt)

    encoded_jwt = jwt_service.create_refresh_jwt(user_dto=_user_dto)
    print(encoded_jwt)

    decoded_jwt = jwt_service.decode_and_validate_type_jwt(token=encoded_jwt)
    print(decoded_jwt)

    print(jwt_service.issue_pair(user_dto=_user_dto))
