from fastapi import APIRouter
from .. import schemas
from ..services import check_voa_srv
import logging


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/check_voa',
    tags=['check voa srv']
)


@router.post("/get",
             response_model=schemas.GetCheckTopologyResponse,
             summary="获取可调光衰数据")
def get_boards(req: schemas.GetBoardRequest):
    print(f"filter: {str(req.filter)}")
    total = check_voa_srv.get_total(req.filter)
    return schemas.GetCheckTopologyResponse(
            data=schemas.CheckTopologyItem(
                myArray=check_voa_srv.get_by_page(req.page_index_begin, req.page_size, req.filter),
                page_index_begin=req.page_index_begin+1,
                page_size=req.page_size,
                total=total,
                page_count=total/req.page_size + 1,
            )
        )


@router.post("/exportData/",
             response_model=schemas.FilterResponse,
             summary="get data for export （实现有错：没有按照当前用户的分配的地区得到下载数据）")
def export_data(req: schemas.ExportRequest):
    return schemas.FilterResponse(
        data=check_voa_srv.get_all(req.filter)
    )
