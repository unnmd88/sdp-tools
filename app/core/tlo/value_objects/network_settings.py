from dataclasses import dataclass
from ipaddress import IPv4Address


@dataclass(frozen=True, slots=True)
class NetworkSettings:
    ipv4: IPv4Address | str | None = None
    gateway: IPv4Address | str | None = None



