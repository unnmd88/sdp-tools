from core.config import settings
from fastapi import APIRouter

from .api_v1 import router as router_api_v1
from .users.routers import router as router_users

router = APIRouter(
    prefix=settings.api.prefix,
)
router.include_router(router_users)
router.include_router(router_api_v1)
