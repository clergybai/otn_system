from fastapi import APIRouter, BackgroundTasks
from .. import schemas
from datetime import datetime
from ..services.computing_srv import get_computing_state, reStartComputed
from apscheduler.schedulers.background import BackgroundScheduler
import logging


logger = logging.getLogger(__name__)

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


@router.get("/startComputed",
            response_model=schemas.StartComputedResponse,
            summary="开始重新计算")
async def start_computed(bg_task: BackgroundTasks):
    if get_computing_state() == 1:
        logger.info(f"{str(datetime.now())}: update in progress.")
        return schemas.StartComputedResponse(
            data=True
        )
    # async start job
    bg_task.add_task(func=reStartComputed)

    return schemas.StartComputedResponse(
        data=True
    )
