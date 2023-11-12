from fastapi import FastAPI
from datetime import datetime, date
from .database import Base, engine
from .routers import get_trouble, post, draw_topo, get_trouble_detail
from common.consts import api_const


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='OTN webapi：transnet 信息获取接口，获取故障信息',
    version=api_const.VERSION
)


def date_handler(obj):
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()


# app.include_router(get_trouble.router, prefix="/webapi")
app.include_router(get_trouble.router)
# app.include_router(draw_topo.router, prefix="/api")
app.include_router(draw_topo.router)
# app.include_router(get_trouble_detail.router, prefix="/api")
app.include_router(get_trouble_detail.router)
app.include_router(post.router)
