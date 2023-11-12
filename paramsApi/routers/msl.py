from fastapi import APIRouter
from .. import schemas
from ..services.msl_srv import (get_msl_by_filter, update,
                                update_wave, get_msl_filter)
from listenningApi.services.computing_srv import get_computing_state


router = APIRouter(
    prefix='/msl',
    tags=['msl']
)


@router.post("/get",
             response_model=schemas.GetBoardResponse,
             summary='get msl data')
def msl_get(req: schemas.MslGetRequest):
    total, items = get_msl_by_filter(**req.dict())
    return schemas.GetBoardResponse(
        data=schemas.BoardItem(
            myArray=items,
            page_index_begin=req.page_index_begin,
            page_size=req.page_size,
            page_count=total / req.page_size,
            total=total,
            is_calculating=get_computing_state()
        )
    )


@router.post("/edit",
             response_model=schemas.GetBoardResponse,
             summary="修改msl")
def edit_msl(req: schemas.MslEditRequest):
    update()
    update_wave(req)
    return schemas.GetBoardResponse(
        data=None
    )


@router.get("/getFilter",
            response_model=schemas.FilterResponse,
            summary="获取msl filter")
def get_filter():
    return schemas.FilterResponse(
        data=get_msl_filter()
    )
