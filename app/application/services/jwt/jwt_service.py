import datetime
from datetime import (
    datetime as dt,
    timedelta as td
)
from typing import AnyStr

import jwt

from application.services.jwt.rules import JWTExpireRules, JWTSecurityRules
from domain.dto.jwt_dto import (
    TokenDataDTO,
    AccessJWTPayloadDTO,
    RefreshJWTPayloadDTO
)
from domain.dto.users import UserDTO
from domain.enums.unsorted import TokenTypesEnum, Organizations, Roles


security_rules = JWTSecurityRules()
expire_rules = JWTExpireRules()


class BaseJWTService:

    expire_minutes_access_token: int = expire_rules.expire_minutes_access_token
    expire_days_refresh_token: int = expire_rules.expire_days_refresh_token
    public_key = security_rules.public_key_path.read_text(encoding="utf-8")
    algorithm = security_rules.algorithm

    @classmethod
    def encode_jwt(
        cls,
        *,
        user_dto: UserDTO,
        token_type: TokenTypesEnum,
        expire_minutes: int = None,
        expire_days: int | None = None,
    ) -> str:
        now = dt.now(datetime.UTC)
        if expire_minutes is not None:
            expire = now + td(minutes=expire_minutes)
        else:
            expire = now + td(days=expire_days)
        service_data = {"exp": expire, "iat": now, "typ": token_type}
        if token_type == TokenTypesEnum.access:
            payload = AccessJWTPayloadDTO(
                user_id=user_dto.id,
                sub=user_dto.username,
                role=user_dto.role,
                organization=user_dto.organization,
                email=user_dto.email,
                **service_data
            )
            assert payload.typ == TokenTypesEnum.access, "Тип токена должен быть access"
        elif token_type == TokenTypesEnum.refresh:
            payload = RefreshJWTPayloadDTO(
                user_id=user_dto.id,
                sub=user_dto.username,
                **service_data,
            )
            assert payload.typ == TokenTypesEnum.refresh, "Тип токена должен быть refresh"
        else:
            #TODO: добавить логирование!
            raise ValueError(f"Неизвестный тип токена: {token_type!r}.")

        return jwt.encode(
            payload=payload.to_dict(),
            key=security_rules.private_key_path.read_text(encoding="utf-8"),
            algorithm=cls.algorithm,
        )

    @classmethod
    def decode_jwt(cls, token: AnyStr) -> AccessJWTPayloadDTO | RefreshJWTPayloadDTO:
        decoded_jwt = jwt.decode(
            jwt=token,
            key=cls.public_key,
            algorithms=[cls.algorithm],
        )
        try:
            token_type = decoded_jwt["typ"]
        except KeyError:
            #TODO: добавить логирование
            raise KeyError("Не найден тип токена в токене при декодировании!!")
        if token_type == TokenTypesEnum.access:
            dto = AccessJWTPayloadDTO
        elif token_type == TokenTypesEnum.refresh:
            dto = RefreshJWTPayloadDTO
        else:
            #TODO: добавить логирование
            raise TypeError(f"Неизвестный тип токена: {token_type}")
        return dto(**decoded_jwt)

    @classmethod
    def create_access_jwt(
        cls,
        *,
        user_dto: UserDTO,
        expire_minutes: int = expire_rules.expire_minutes_access_token,
    ) -> str:
        return cls.encode_jwt(
            user_dto=user_dto,
            token_type=TokenTypesEnum.access,
            expire_minutes=expire_minutes,
        )

    @classmethod
    def create_refresh_jwt(
        cls,
        *,
        user_dto: UserDTO,
        expire_days: int = expire_rules.expire_days_refresh_token,
    ) -> str:
        return cls.encode_jwt(
            user_dto=user_dto,
            token_type=TokenTypesEnum.refresh,
            expire_days=expire_days,
        )

    @classmethod
    def issue_access_jwt(
        cls,
        user_dto: UserDTO,
        expire_minutes_access: int = expire_rules.expire_minutes_access_token,
    ) -> TokenDataDTO:
        return TokenDataDTO(
            access_token=cls.create_access_jwt(user_dto=user_dto, expire_minutes=expire_minutes_access),
            refresh_token=None,
        )

    @classmethod
    def issue_pair(
        cls,
        user_dto: UserDTO,
        expire_minutes_access: int = expire_rules.expire_minutes_access_token,
        expire_days_refresh: int = expire_rules.expire_days_refresh_token,
    ) -> TokenDataDTO:
        return TokenDataDTO(
            access_token=cls.create_access_jwt(user_dto=user_dto, expire_minutes=expire_minutes_access),
            refresh_token=cls.create_refresh_jwt(user_dto=user_dto, expire_days=expire_days_refresh)
        )


if __name__ == '__main__':
    _user_dto = UserDTO(
        id=1,
        firstname="Junker",
        lastname="Junker",
        username="test",
        role=Roles.superuser,
        organization=Organizations.SDP,
        email="test@test.com",
        is_active=True,
        phone_number=None,
        telegram="test_telegram",
        description="test_description",
    )
    print(_user_dto)

    encoded_jwt = BaseJWTService.create_access_jwt(user_dto=_user_dto)
    print(encoded_jwt)

    decoded_jwt = BaseJWTService.decode_jwt(token=encoded_jwt)
    print(decoded_jwt)

    encoded_jwt = BaseJWTService.create_refresh_jwt(user_dto=_user_dto)
    print(encoded_jwt)

    decoded_jwt = BaseJWTService.decode_jwt(token=encoded_jwt)
    print(decoded_jwt)

    print(BaseJWTService.issue_pair(user_dto=_user_dto))

