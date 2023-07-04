from fastapi import APIRouter
from .. import schemas
from ..services.computing_srv import get_computing_state


router = APIRouter(
    prefix='/PGListening',
    tags=['PG Listening']
)


@router.get("/getComputedState",
            response_model=schemas.ComputedStateResponse,
            summary="获取目前计算状态")
def get_computed_state():
    return schemas.ComputedStateResponse(
        data=get_computing_state()
    )
