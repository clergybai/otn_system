from fastapi import APIRouter, status, File, UploadFile
from .. import schemas
from ..services.filter_srv import get_all_filters, get_board_by_page, get_board_total, add_board_info
from listenningApi.services.computing_srv import get_computing_state
from common.config import settings
from datetime import datetime
import pytz
import logging


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/oa_board_standard',
    tags=['oa board standard']
)


@router.get("/getFilter",
            response_model=schemas.FilterResponse,
            summary="返回过滤条件")
def get_filter():
    return schemas.FilterResponse(
        data=get_all_filters()
    )


@router.post("/get",
             response_model=schemas.GetBoardResponse,
             summary="Get board")
def get_boards(req: schemas.GetBoardRequest):
    print(f"filter: {str(req.filter)}")
    total = get_board_total(req.filter)
    return schemas.GetBoardResponse(
            data=schemas.BoardItem(
                myArray=get_board_by_page(req.page_index_begin, req.page_size, req.filter),
                page_index_begin=req.page_index_begin+1,
                page_size=req.page_size,
                total=total,
                page_count=total/req.page_size + 1,
                is_calculating=get_computing_state()
            )
        )


@router.post("/add",
             response_model=schemas.AddOaBoardStandardResponse,
             summary="添加板卡信息")
def add_board(req: schemas.AddOaBoardStandardRequest):
    result = add_board_info(req.dict())
    if result:
        return schemas.AddOaBoardStandardResponse(
            data=None
        )
    else:
        return schemas.AddOaBoardStandardResponse(
            code_type=status.HTTP_400_BAD_REQUEST,
            code=status.HTTP_400_BAD_REQUEST,
            data=None,
            msg="客户端请求的语法错误，服务器无法理解。"
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
        temp_file = settings.path_import_in_optical_amplifier_type
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
