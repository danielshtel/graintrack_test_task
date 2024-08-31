from fastapi import APIRouter

from app.interfaces.api import (
    auth,
    category
)

from app.core.config import settings

router = APIRouter(prefix=settings.API_V1_PREFIX)

router.include_router(auth.router)
router.include_router(category.router)
