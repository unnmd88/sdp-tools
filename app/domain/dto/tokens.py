from dataclasses import dataclass

from domain.users.entities.user import UserEntity


@dataclass(slots=True, frozen=True, kw_only=True)
class IssueJWTDTO:
    user_entity: UserEntity
    access_token: bool = True
    refresh_token: bool = False


@dataclass(slots=True, frozen=True, kw_only=True)
class TokenDataDTO:
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
