from fastapi import APIRouter
from .. import schemas
from ..services.filter_srv import get_board_type_by_page, get_board_type_total
from listenningApi.services.computing_srv import get_computing_state

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
