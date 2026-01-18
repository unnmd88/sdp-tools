from typing import Protocol


class UserPasswordServiceProtocol(Protocol):
    @classmethod
    def hash_password(cls, password: str) -> bytes: ...

    @classmethod
    def verify_password(cls, *, password: str, hashed_password: bytes) -> bool: ...

    @classmethod
    def generate_password(cls) -> str: ...
