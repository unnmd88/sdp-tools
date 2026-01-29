from dataclasses import dataclass, asdict
from datetime import timedelta, datetime

from domain.enums.unsorted import Roles, Organizations
from domain.entities.user import UserEntity


@dataclass(slots=True, frozen=True, kw_only=True)
class TokenDataDTO:
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


@dataclass(slots=True, frozen=True, kw_only=True)
class RefreshJWTPayloadDTO:
    user_id: int
    sub: str
    typ: str
    exp: int | datetime
    iat: int | datetime

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(slots=True, frozen=True, kw_only=True)
class AccessJWTPayloadDTO(RefreshJWTPayloadDTO):
    role: str
    organization: str
    email: str | None


@dataclass(slots=True, frozen=True, kw_only=True)
class PayloadJWTDTO:
    user_id: int
    sub: str
    email: str | None = None
    role: Roles | None = None
    organization: Organizations | None = None

