from core.config import settings
from fastapi import APIRouter

# from core.users import router as users_router
from presentation.api.auth.routes import router as auth_router

from .passport_groups.routes import router as passport_groups_router
from .passports.routes import router as passports_router
from .regions.routes import router as regions_router
from .tlo.routes import router as tlo_router

router = APIRouter(prefix=settings.api.v1.prefix)
router.include_router(auth_router)
# router.include_router(users_router)
router.include_router(auth_router)
router.include_router(tlo_router)
router.include_router(regions_router)
router.include_router(passport_groups_router)
router.include_router(passports_router)
