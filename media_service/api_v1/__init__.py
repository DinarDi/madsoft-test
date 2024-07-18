from fastapi import APIRouter

from .media.views import media_router


router = APIRouter()
router.include_router(router=media_router, prefix='/media')
