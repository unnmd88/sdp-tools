import uvicorn
from api import router as api_v1_router
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.config import settings

app = FastAPI()
app.include_router(router=api_v1_router)


app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://192.168.45.66", "http://192.168.45.90"],  # или ["http://localhost:5173", "http://твой_домен"]
    allow_origins=['*'],  # или ["http://localhost:5173", "http://твой_домен"]
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


if __name__ == '__main__':
    uvicorn.run('main:app', **settings.run.model_dump())
