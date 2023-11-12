from .. import schemas
from fastapi import APIRouter
from ..services.order_list_srv import OrderListService
from listenningApi.services.computing_srv import get_computing_state
from datetime import datetime, timedelta


router = APIRouter(
    prefix='/GetTrouble',
    tags=['GetTrouble'],
)


@router.post("/getTrouble",
             response_model=schemas.GetTroubleResponse,
             summary="get trouble by filter")
def get_trouble(req: schemas.TroubleSearchRequest):
    json = req
    print(f"json: {str(json)}")
    total, items = OrderListService.get_trouble_by_filter(**req.dict())
    return schemas.GetTroubleResponse(
        data=schemas.BoardItem(
            myArray=items,
            page_index_begin=req.page_index_begin,
            page_size=req.page_size,
            page_count=total / req.page_size,
            total=total,
            is_calculating=get_computing_state()
        )
    )
    

@router.get("/exportOrderListData/",
            response_model=schemas.GetTroubleStatisticsResponse,
            summary="get trouble for export （实现有错：没有按照当前用户的分配的地区得到下载数据）")
def export_order_list_data():
    current_date = datetime.now()
    six_months_ago = current_date - timedelta(days=182)
    formatted_date_str = six_months_ago.strftime("%Y-%m-%d %H:%M:%S")
    current_date_str = current_date.strftime("%Y-%m-%d %H:%M:%S")
    times_arr = {
        'startTime': formatted_date_str,
        'endTime': current_date_str
    }
    filters = {
        "param": {
            'timesArr': times_arr
        }
    }

    total, items = OrderListService.get_trouble_by_filter(**filters)
    return schemas.GetTroubleStatisticsResponse(
        data=items
    )
