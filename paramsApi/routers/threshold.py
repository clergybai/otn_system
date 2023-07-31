from fastapi import APIRouter, status
from .. import schemas
from datetime import datetime
from ..services.threshold_srv import (get_default, get_outline, get_threshold_total, get_input_thread, 
                                      upsert, get_specific_threshold, update_specific_threshold,
                                      delete_threshold)
from listenningApi.services.computing_srv import get_computing_state


router = APIRouter(
    prefix='/Threshold',
    tags=['Threshold']
)


@router.get("/get_default",
            response_model=schemas.GetDefaultThreadResponse,
            summary="default threshold")
def get_default_threshold():
    d = get_default()
    return schemas.GetDefaultThreadResponse(
        data={
            "oa_input_power_fluc_risk_thr": d.oa_input_power_fluc_risk_thr,
            "oa_input_power_fluc_risk_maj": d.oa_input_power_fluc_risk_maj,
            "oa_input_power_fluc_risk_urg": d.oa_input_power_fluc_risk_urg,
            "oa_output_power_fluc_risk_thr": d.oa_output_power_fluc_risk_thr,
            "oa_output_power_fluc_risk_maj": d.oa_output_power_fluc_risk_maj,
            "oa_output_power_fluc_risk_urg": d.oa_output_power_fluc_risk_urg,
            "oa_gain_std_dev_up_risk_thr": d.oa_gain_std_dev_up_risk_thr,
            "oa_gain_std_dev_up_risk_maj": d.oa_gain_std_dev_up_risk_maj,
            "oa_gain_std_dev_up_risk_urg": d.oa_gain_std_dev_up_risk_urg,
            "oa_gain_std_dev_low_risk_thr": d.oa_gain_std_dev_low_risk_thr,
            "oa_gain_std_dev_low_risk_maj": d.oa_gain_std_dev_low_risk_maj,
            "oa_gain_std_dev_low_risk_urg": d.oa_gain_std_dev_low_risk_urg,
            "oa_input_power_std_dev_up_risk_thr": d.oa_input_power_std_dev_up_risk_thr,
            "oa_input_power_std_dev_up_risk_maj": d.oa_input_power_std_dev_up_risk_maj,
            "oa_input_power_std_dev_up_risk_urg": d.oa_input_power_std_dev_up_risk_urg,
            "oa_input_power_std_dev_low_risk_thr": d.oa_input_power_std_dev_low_risk_thr,
            "oa_input_power_std_dev_low_risk_maj": d.oa_input_power_std_dev_low_risk_maj,
            "oa_input_power_std_dev_low_risk_urg": d.oa_input_power_std_dev_low_risk_urg,
            "oa_output_power_std_dev_up_risk_thr": d.oa_output_power_std_dev_up_risk_thr,
            "oa_output_power_std_dev_up_risk_maj": d.oa_output_power_std_dev_up_risk_maj,
            "oa_output_power_std_dev_up_risk_urg": d.oa_output_power_std_dev_up_risk_urg,
            "oa_output_power_std_dev_low_risk_thr": d.oa_output_power_std_dev_low_risk_thr,
            "oa_output_power_std_dev_low_risk_maj": d.oa_output_power_std_dev_low_risk_maj,
            "oa_output_power_std_dev_low_risk_urg": d.oa_output_power_std_dev_low_risk_urg,
            "fiber_two_way_dev_risk_thr": d.fiber_two_way_dev_risk_thr,
            "fiber_two_way_dev_risk_maj": d.fiber_two_way_dev_risk_maj,
            "fiber_two_way_dev_risk_urg": d.fiber_two_way_dev_risk_urg,
            "olp_power_dev_risk_thr": d.olp_power_dev_risk_thr,
            "olp_power_dev_risk_maj": d.olp_power_dev_risk_maj,
            "olp_power_dev_risk_urg": d.olp_power_dev_risk_urg,
            "city": d.city,
            "net_level": d.net_level,
            "owner": d.owner,
            "is_used": d.is_used,
            "is_used_bool": True if d.is_used > 0 else False,
            "rule_name": d.rule_name
        }
    )


@router.post("/get_outline",
             response_model=schemas.GetBoardResponse,
             summary="Get outline")
def get_threshold_outline(req: schemas.GetBoardRequest):
    total = get_threshold_total(req.filter)
    return schemas.GetBoardResponse(
        data=schemas.BoardItem(
            myArray=get_outline(req.page_index_begin, req.page_size, req.filter),
            page_index_begin=req.page_index_begin+1,
            page_size=req.page_size,
            total=total,
            page_count=total/req.page_size + 1,
            is_calculating=get_computing_state()
        )
    )


@router.post("/get_rule_with_name",
             response_model=schemas.GetRuleWithNameResponse,
             summary="get_rule_with_name")
def get_rule_with_name(req: schemas.GetRuleWithNameRequest):
    t = get_input_thread(rule_name=req.rule_name, is_history=2)
    if t is None:
        t = get_input_thread(rule_name=req.rule_name)
    rtn = None
    if t:
        rtn = {
            "oa_input_power_fluc_risk_thr": t.oa_input_power_fluc_risk_thr,
            "oa_input_power_fluc_risk_maj": t.oa_input_power_fluc_risk_maj,
            "oa_input_power_fluc_risk_urg": t.oa_input_power_fluc_risk_urg,
            "oa_output_power_fluc_risk_thr": t.oa_output_power_fluc_risk_thr,
            "oa_output_power_fluc_risk_maj": t.oa_output_power_fluc_risk_maj,
            "oa_output_power_fluc_risk_urg": t.oa_output_power_fluc_risk_urg,
            "oa_gain_std_dev_up_risk_thr": t.oa_gain_std_dev_up_risk_thr,
            "oa_gain_std_dev_up_risk_maj": t.oa_gain_std_dev_up_risk_maj,
            "oa_gain_std_dev_up_risk_urg": t.oa_gain_std_dev_up_risk_urg,
            "oa_gain_std_dev_low_risk_thr": t.oa_gain_std_dev_low_risk_thr,
            "oa_gain_std_dev_low_risk_maj": t.oa_gain_std_dev_low_risk_maj,
            "oa_gain_std_dev_low_risk_urg": t.oa_gain_std_dev_low_risk_urg,
            "oa_input_power_std_dev_up_risk_thr": t.oa_input_power_std_dev_up_risk_thr,
            "oa_input_power_std_dev_up_risk_maj": t.oa_input_power_std_dev_up_risk_maj,
            "oa_input_power_std_dev_up_risk_urg": t.oa_input_power_std_dev_up_risk_urg,
            "oa_input_power_std_dev_low_risk_thr": t.oa_input_power_std_dev_low_risk_thr,
            "oa_input_power_std_dev_low_risk_maj": t.oa_input_power_std_dev_low_risk_maj,
            "oa_input_power_std_dev_low_risk_urg": t.oa_input_power_std_dev_low_risk_urg,
            "oa_output_power_std_dev_up_risk_thr": t.oa_output_power_std_dev_up_risk_thr,
            "oa_output_power_std_dev_up_risk_maj": t.oa_output_power_std_dev_up_risk_maj,
            "oa_output_power_std_dev_up_risk_urg": t.oa_output_power_std_dev_up_risk_urg,
            "oa_output_power_std_dev_low_risk_thr": t.oa_output_power_std_dev_low_risk_thr,
            "oa_output_power_std_dev_low_risk_maj": t.oa_output_power_std_dev_low_risk_maj,
            "oa_output_power_std_dev_low_risk_urg": t.oa_output_power_std_dev_low_risk_urg,
            "fiber_two_way_dev_risk_thr": t.fiber_two_way_dev_risk_thr,
            "fiber_two_way_dev_risk_maj": t.fiber_two_way_dev_risk_maj,
            "fiber_two_way_dev_risk_urg": t.fiber_two_way_dev_risk_urg,
            "olp_power_dev_risk_thr": t.olp_power_dev_risk_thr,
            "olp_power_dev_risk_maj": t.olp_power_dev_risk_maj,
            "olp_power_dev_risk_urg": t.olp_power_dev_risk_urg,
            "city": t.city,
            "net_level": t.net_level,
            "owner": t.owner,
            "is_used": t.is_used,
            "is_used_bool": True if t.is_used > 0 else False,
            "rule_name": t.rule_name
        }

    code_type = status.HTTP_204_NO_CONTENT if rtn is None else status.HTTP_200_OK
    msg = "请求成功。" if code_type == status.HTTP_200_OK else "无内容。服务器成功处理，但未返回内容。"
    return schemas.GetRuleWithNameResponse(
        code_type=code_type,
        code=code_type,
        msg=msg,
        data=rtn
    )


@router.post("/update_rule",
             response_model=schemas.GetBoardResponse,
             summary="update rule")
def update_rule(req: dict):
    result = upsert(**req)
    code_type = status.HTTP_200_OK
    code = status.HTTP_200_OK
    msg = ""
    data = None
    if isinstance(result, bool):
        code_type = status.HTTP_200_OK if result else status.HTTP_304_NOT_MODIFIED
        code = code_type
        msg = "请求成功。" if result else "未修改。所请求的资源未修改。"
    else:
        msg = "请求成功。"

    return schemas.GetBoardResponse(
        code_type=code_type,
        code=code,
        msg=msg,
        data=data
    )


@router.post("/update_status_used",
             response_model=schemas.GetRuleWithNameResponse,
             summary="update status")
def update_status_used(req: dict):
    city = req['city']
    is_used_bool = req['is_used_bool']
    rule_name = req['rule_name']
    code_type = status.HTTP_304_NOT_MODIFIED
    code = code_type
    msg = "未修改。所请求的资源未修改。"
    # TODO: update_status_used, 如果是设置为启用，首先查到没启用的
    if is_used_bool:
        thread = get_specific_threshold(city=city, rule_name=rule_name, is_history=2)
        if thread:
            update_specific_threshold(city=city, rule_name=rule_name, is_history=2)
    is_updated = upsert(rule_name=rule_name, is_used=int(is_used_bool), timestamp=datetime.now())
    if is_updated:
        code_type = status.HTTP_200_OK
        code = code_type
    return schemas.GetRuleWithNameResponse(
        code_type=code_type,
        code=code,
        msg=msg,
        data=None
    )


@router.post("/delete_rule",
             response_model=schemas.GetBoardResponse,
             summary="删除规则")
def delete_rule(req: schemas.GetRuleWithNameRequest):
    if len(req.rule_name) == 0:
        return schemas.GetBoardResponse(
            code=status.HTTP_400_BAD_REQUEST,
            data=None
        )
    result = delete_threshold(req.rule_name)
    return schemas.GetBoardResponse(
        code= status.HTTP_200_OK if result else status.HTTP_400_BAD_REQUEST,
        data=None
    )
