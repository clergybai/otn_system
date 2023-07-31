from fastapi import APIRouter
from .. import schemas
from ..services.base_line_srv import get_default


router = APIRouter(
    prefix='/base_line',
    tags=['base line']
)


@router.get("/get_default",
            response_model=schemas.GetDefaultStdValueResponse,
            summary="default input std value")
def get_std_value_default():
    default = get_default()
    return schemas.GetDefaultStdValueResponse(
        data=schemas.StdValueItem(
            optical_power_baseline=default.optical_power_baseline,
            gain_baseline=default.gain_baseline,
            olp_act_stand_baseline=default.olp_act_stand_baseline,
            cable_in_out_baseline=default.cable_in_out_baseline
        )
    )
