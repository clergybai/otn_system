import uvicorn
from fastapi import FastAPI
from .database import (Base, lo_engine,)
from .routers import (permissions, login, log, user)
from common.consts import api_const
from common.config import settings


Base.metadata.create_all(bind=lo_engine)

if settings.env == 'dev':
    app = FastAPI(
        title='OTN loginApi：登陆，身份验证, 权限相关接口',
        version=api_const.VERSION,
    )
else:
    app = FastAPI(
        title='OTN loginApi：登陆，身份验证, 权限相关接口',
        version=api_const.VERSION,
        docs_url=None,
        redoc_url=None
    )


# PREFIX = "/loginApi"
# app.include_router(permissions.router, prefix=PREFIX)
# app.include_router(login.router, prefix=PREFIX)
# app.include_router(log.router, prefix=PREFIX)
# app.include_router(user.router, prefix=PREFIX)
app.include_router(permissions.router)
app.include_router(login.router)
app.include_router(log.router)
app.include_router(user.router)
