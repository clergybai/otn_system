from fastapi import APIRouter
from .. import schemas
from ..services.filter_srv import get_voa_config_by_page, get_voa_config_total
from listenningApi.services.computing_srv import get_computing_state


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
