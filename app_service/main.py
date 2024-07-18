from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from fastapi import FastAPI

from database import db_manager
from core import settings
from api_v1 import router as router_v1


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    db_manager.init_connection(db_url=settings.DB_URL)
    yield
    await db_manager.close_connection()


memes_app = FastAPI(lifespan=lifespan)
memes_app.include_router(router_v1, prefix='/api/v1')


if __name__ == '__main__':
    uvicorn.run(
        'main:memes_app',
        reload=True,
    )
