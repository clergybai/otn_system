from fastapi import FastAPI
from common.consts import api_const
from .routers import oa_board_standard, oa_board_type, voa_config, base_line, threshold, msl


app = FastAPI(
    title='OTN paramsApi：参数相关接口',
    version=api_const.VERSION
)

PREFIX = "/paramsApi"
app.include_router(oa_board_standard.router, prefix=PREFIX)
app.include_router(oa_board_type.router, prefix=PREFIX)
app.include_router(voa_config.router, prefix=PREFIX)
app.include_router(base_line.router, prefix=PREFIX)
app.include_router(threshold.router, prefix=PREFIX)
app.include_router(msl.router, prefix=PREFIX)
