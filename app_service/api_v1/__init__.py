from fastapi import APIRouter

from .memes.views import memes_router


router = APIRouter()
router.include_router(router=memes_router, prefix='/memes')
