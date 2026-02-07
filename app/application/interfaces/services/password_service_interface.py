from typing import Protocol


class PasswordServiceProtocol(Protocol):
    """Протокол сервиса для работы с паролями."""

    @classmethod
    def hash_password(cls, password: str) -> bytes: ...

    @classmethod
    def verify_password(cls, *, password: str, hashed_password: bytes) -> bool: ...
