from fastapi import APIRouter, status
from .. import schemas
from datetime import datetime
from ..services import threshold_och_srv
from listenningApi.services.computing_srv import get_computing_state

router = APIRouter(
    prefix='/Threshold_och',
    tags=['Threshold Och']
)


@router.post("/get_outline",
             response_model=schemas.GetBoardResponse,
             summary="Get outline")
def get_threshold_outline(req: schemas.GetBoardRequest):
    total = threshold_och_srv.get_threshold_och_total(req.filter)
    return schemas.GetBoardResponse(
        data=schemas.BoardItem(
            myArray=threshold_och_srv.get_outline(req.page_index_begin,
                                                  req.page_size, req.filter),
            page_index_begin=req.page_index_begin+1,
            page_size=req.page_size,
            total=total,
            page_count=total/req.page_size + 1,
            is_calculating=get_computing_state()
        )
    )
