from auth.routes import router as auth_router
from core.config import settings
from fastapi import APIRouter
from users.routes import router as users_router
from .tlo.routes import router as tlo_router
from .regions.routes import router as regions_router

router = APIRouter(prefix=settings.api.v1.prefix)
router.include_router(auth_router)
router.include_router(users_router)
router.include_router(tlo_router)
router.include_router(regions_router)
