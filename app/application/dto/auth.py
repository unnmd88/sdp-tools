from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class UserAuthDTO:
    username: str
    password: str
