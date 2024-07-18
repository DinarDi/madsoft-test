import uvicorn
from fastapi import FastAPI
from api_v1 import router as router_v1


media_app = FastAPI()
media_app.include_router(router_v1, prefix='/api/v1')

if __name__ == '__main__':
    uvicorn.run(
        'main:media_app',
        reload=True,
    )
