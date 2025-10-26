import uvicorn

from app.core.config import settings
from fastapi import FastAPI
from users.demo import router as demo_auth_router


app = FastAPI()
# app.include_router(router=router_v1, prefix=settings.api_v1_prefix)
app.include_router(router=demo_auth_router, prefix=settings.api.v1.prefix)


@app.get('/')
def root():
    # print(a_sess)
    return {'Message': 'Hello sdp-tools api'}

# app.include_router(routr)

if __name__ == '__main__':
    uvicorn.run('main:app', **settings.run.model_dump())