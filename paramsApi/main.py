from fastapi import FastAPI
from common.consts import api_const
from .routers import (oa_board_standard, oa_board_type, voa_config, base_line, threshold,
                      msl, pm_mca, check_topology, check_optical_ne, check_oa_board_type,
                      check_voa, check_pm, threshold_och)


app = FastAPI(
    title='OTN paramsApi：参数相关接口',
    version=api_const.VERSION
)

# PREFIX = "/paramsApi"
# app.include_router(oa_board_standard.router, prefix=PREFIX)
# app.include_router(oa_board_type.router, prefix=PREFIX)
# app.include_router(voa_config.router, prefix=PREFIX)
# app.include_router(base_line.router, prefix=PREFIX)
# app.include_router(threshold.router, prefix=PREFIX)
# app.include_router(msl.router, prefix=PREFIX)
app.include_router(oa_board_standard.router)
app.include_router(oa_board_type.router)
app.include_router(voa_config.router)
app.include_router(base_line.router)
app.include_router(threshold.router)
app.include_router(msl.router)
app.include_router(pm_mca.router)
app.include_router(check_topology.router)
app.include_router(check_optical_ne.router)
app.include_router(check_oa_board_type.router)
app.include_router(check_voa.router)
app.include_router(check_pm.router)
app.include_router(threshold_och.router)
