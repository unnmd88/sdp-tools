from typing import Protocol


class AuthServiceProtocol(Protocol):
    def authenticate(
        self,
        *,
        plain_password: str,
        hashed_password: bytes
    ) -> bool: ...

