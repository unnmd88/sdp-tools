from dataclasses import dataclass
from typing import Protocol


@dataclass
class AuthenticationSchemaProtocol(Protocol):
    username: str
    password: str




