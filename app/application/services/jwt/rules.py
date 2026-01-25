from dataclasses import dataclass
from pathlib import Path

from core.config import BASE_DIR


@dataclass(slots=True, frozen=True, kw_only=True)
class JWTSecurityRules:
    private_key_path: Path = BASE_DIR / "certs" / "private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "public.pem"
    algorithm: str = "RS256"


@dataclass(slots=True, frozen=True, kw_only=True)
class JWTExpireRules:
    expire_minutes_access_token: int = 15
    expire_days_refresh_token: int = 1
