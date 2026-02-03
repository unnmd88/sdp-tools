import uvicorn
from presentation.api import router as api_v1_router
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core.config import settings
from presentation.api.middlewares.decode_jwt_middleware import JWTMiddleware
from presentation.api.error_handling import setup_exception_handlers

app = FastAPI(
    title="Api для работы с паспортами светофорного объекта.",
)
app.include_router(router=api_v1_router)


app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://192.168.45.66", "http://192.168.45.90"],  # или ["http://localhost:5173", "http://твой_домен"]
    allow_origins=["*"],  # или ["http://localhost:5173", "http://твой_домен"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.add_middleware(
#     JWTMiddleware,
#     app,
# )

setup_exception_handlers(app)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.run.reload,
    )
