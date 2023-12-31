from fastapi import FastAPI
import uvicorn
from common.consts import api_const
from .routers import pg_listening


app = FastAPI(
    title='OTN listenningApi：listenning服务相关接口',
    version=api_const.VERSION
)

PREFIX = "/listenningApi"
app.include_router(pg_listening.router, prefix=PREFIX)


if __name__ == "__main__":
    uvicorn.run("listenningApi.main:app", host='0.0.0.0', port='39966', reload=True)
