from dataclasses import dataclass
from ipaddress import IPv4Address, IPv4Network


@dataclass(frozen=True, slots=True)
class NetworkSettings:
    ipv4: IPv4Address | str | None = None
    network: IPv4Network | None = None
    mask: IPv4Address | str | None = None
    gateway: IPv4Address | str | None = None
    broadcast: IPv4Address | str | None = None
    mac_address: str | None = None
