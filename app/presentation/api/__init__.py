from core.config import settings
from fastapi import APIRouter

from .api_v1 import router as router_api_v1
from .users.routers import router as router_users
from .auth.routes import router as router_auth
from .auth.admin.routes import router as administration_router

router = APIRouter(prefix=settings.api.prefix)

router.include_router(router_auth)
router.include_router(administration_router)
router.include_router(router_users)
router.include_router(router_api_v1)
