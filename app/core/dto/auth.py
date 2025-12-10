from dataclasses import dataclass


@dataclass(kw_only=True)
class UserAuthDTO:
    username: str
    password: str