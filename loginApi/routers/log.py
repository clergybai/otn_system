from fastapi import APIRouter
from .. import schemas
from ..models.sys_log import SysLog
import uuid
from datetime import datetime


router = APIRouter(
    prefix='/OperationLog',
    tags=['OperationLog']
)


@router.post("/setLog/",
             response_model=schemas.SetLogResponse,
             summary="登录操作log")
def set_log(req: schemas.SetLogRequest):
    log = SysLog(
        id=str(uuid.uuid4()),
        op_user=req.op_user,
        op_module=req.op_module,
        op_behavior=req.op_behavior)
    SysLog.add_log(log)
    return schemas.SetLogResponse(
        data=True
    )


@router.post("/getLog/",
             response_model=schemas.DataListResponse,
             summary="Get operation logs")
def get_log(req: schemas.LogRequest):
    request_json = req.dict()
    search_json = {}
    date_format = '%Y-%m-%d %H:%M:%S'
    for key, val in request_json.items():
        if val and len(val) > 0:
            if val.lower().find('time') > 0:
                search_json[key] = datetime.strptime(val, date_format)
            else:
                search_json[key] = val
                
    print(f"search_json: {str(search_json)}")
    logs = SysLog.get_log(**search_json)

    return schemas.DataListResponse(
        data=[log.to_dict() for log in logs]
        )
