from fastapi import APIRouter, File, UploadFile
from .. import schemas
from ..services.filter_srv import (get_voa_config_by_page,
                                   get_voa_config_total, get_voa_config_filter)
from listenningApi.services.computing_srv import get_computing_state
from common.config import settings
from datetime import datetime
import pytz
import logging


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/voa_config',
    tags=['voa config']
)


@router.post("/get",
             response_model=schemas.GetBoardResponse,
             summary="Get voa configs")
def get_voa_configs(req: schemas.GetBoardRequest):
    total = get_voa_config_total(req.filter)
    return schemas.GetBoardResponse(
            data=schemas.BoardItem(
                myArray=get_voa_config_by_page(req.page_index_begin, req.page_size, req.filter),
                page_index_begin=req.page_index_begin+1,
                page_size=req.page_size,
                total=total,
                page_count=total/req.page_size + 1,
                is_calculating=get_computing_state()
            )
        )


@router.post("/upload_file",
             response_model=schemas.UploadFileResponse,
             summary="Get voa config filter")
async def upload_file(file: UploadFile = File(...)):
    try:
        res = await file.read()
        current_time = datetime.now()
        local_timezone = pytz.timezone('Asia/Shanghai')
        local_time = current_time.astimezone(local_timezone)
        temp_file = settings.path_import_in_voa_config
        idx = temp_file.index(".xlsx")
        formatted_time = local_time.strftime("%Y%m%d%H%M%S")
        save_file = f"{temp_file[0:idx]}{formatted_time}.xlsx"

        with open(save_file, "wb") as f:
            f.write(res)
        return schemas.UploadFileResponse(data=None)
    except Exception as e:
        logger.exception(e)
        return schemas.UploadFileResponse(
            data="fail"
        )


@router.get("/getFilter",
            response_model=schemas.FilterResponse,
            summary="get voa_config filter")
def get_filter():
    return schemas.FilterResponse(
        data=get_voa_config_filter()
    )
