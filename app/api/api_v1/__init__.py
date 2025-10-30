from auth.routes import router as auth_router
from core.config import settings
from fastapi import APIRouter
from users.routes import router as users_router

router = APIRouter(prefix=settings.api.v1.prefix)
router.include_router(auth_router)
router.include_router(users_router)
