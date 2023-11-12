from fastapi import APIRouter, File, UploadFile
from .. import schemas
from ..services.filter_srv import (get_board_type_by_page,
                                   get_board_type_total, get_board_type_filter)
from listenningApi.services.computing_srv import get_computing_state
from common.config import settings
from datetime import datetime
import pytz
import logging


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/oa_board_type',
    tags=['oa board type']
)


@router.post("/get",
             response_model=schemas.GetBoardResponse,
             summary="Get board type")
def get_board_types(req: schemas.GetBoardRequest):
    print(f"filter: {str(req.filter)}")
    total = get_board_type_total(req.filter)
    return schemas.GetBoardResponse(
            data=schemas.BoardItem(
                myArray=get_board_type_by_page(req.page_index_begin, req.page_size, req.filter),
                page_index_begin=req.page_index_begin+1,
                page_size=req.page_size,
                total=total,
                page_count=total/req.page_size + 1,
                is_calculating=get_computing_state()
            )
        )


@router.post("/upload_file",
             response_model=schemas.UploadFileResponse,
             summary="upload file...")
async def upload_file(file: UploadFile = File(...)):
    try:
        res = await file.read()
        current_time = datetime.now()
        local_timezone = pytz.timezone('Asia/Shanghai')
        local_time = current_time.astimezone(local_timezone)
        temp_file = settings.path_import_in_board_config_data
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
            summary="get board type threshold")
def get_filter():
    return schemas.FilterResponse(
        data=get_board_type_filter()
    )
