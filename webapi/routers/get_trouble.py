from .. import schemas
from typing import List
from fastapi import APIRouter
from ..services.order_list_srv import (OrderListService, get_order_list_filter,
                                       get_order_list_filter_later_part, get_filter_citys)


router = APIRouter(
    prefix='/GetTrouble',
    tags=['GetTrouble'],
)


@router.post("/order_list/")
def get_order_list(order_list_req: schemas.OrderListRequest):
    srv = OrderListService(**order_list_req.dict())
    srv.get_handled_data([], deal_all=True)
    resp = {}
    resp['unhandled'] = srv.get_unhandled()
    resp['statistics'] = srv.get_statistics()
    resp['network_level'] = srv.get_network_level()
    resp['city_group'] = srv.get_city_statistics()
    resp['annual_statistics'] = srv.get_annual_statistics()
    resp['city_statistics'] = srv.get_city_risk_level_statistics()
    return resp


@router.post("/unhandled/", response_model=schemas.GetTroubleUnhandleResponse, description="取得未处理数据")
def get_unhandled(order_list_req: schemas.OrderListRequest):
    datas = OrderListService.getTop_end(order_list_req)
    rtn = None
    for item in datas:
        rtn = item
    return schemas.GetTroubleUnhandleResponse(data={"val": rtn.top_endCount,
                                                    "max": rtn.tabCount})


@router.post("/Statistics/", response_model=schemas.GetTroubleStatisticsResponse)
def get_statistics(order_list_req: schemas.OrderListRequest):
    # srv = OrderListService(**order_list_req.dict())
    # srv.get_handled_data(['statistics'])
    datas = OrderListService.getRisk_typeGroup(order_list_req)
    troubles = []
    for item in datas:
        risk_type = item.risk_type
        count = item.count
        if "过低" in risk_type or "过高" in risk_type:
            content = risk_type.replace("过高", "").replace("过低", "") + "超标"
            trouble = next((t for t in troubles if t['name'] == content), None)
            if trouble is not None:
                trouble['count'] += count
            else:
                troubles.append({
                    "count": count,
                    "name": content
                })
        else:
            troubles.append({
                "count": item.count,
                "name": item.risk_type
                })
    ret = []
    for item in troubles:
        ret.append({
            "value": item['count'],
            "count": item['count'],
            "name": item['name'],
            "content": item['name']
        })
    return schemas.GetTroubleStatisticsResponse(data=ret)


@router.post("/level/", response_model=schemas.GetTroubleStatisticsResponse)
def get_network_level(order_list_req: schemas.OrderListRequest):
    # srv = OrderListService(**order_list_req.dict())
    # srv.get_handled_data(['network_level'])
    datas = OrderListService.getNetwork_levelGroup(order_list_req)
    troubles = []
    for item in datas:
        troubles.append({
            "count": item.count,
            "name": item.network_level
        })
    ret = []
    for item in troubles:
        ret.append({
            "value": item['count'],
            "count": item['count'],
            "name": item['name'],
            "content": item['name']
        })

    return schemas.GetTroubleStatisticsResponse(data=ret)


@router.get("/cityHiddenGroup", response_model=schemas.GetTroubleStatisticsResponse)
def get_city_hidden_group():
    # srv = OrderListService(startTime=None, endTime=None, city=None, network_level='all')
    # srv.get_handled_data(['city_group'])
    datas = OrderListService.getHiddenCityGroup()
    troubles = []
    for item in datas:
        troubles.append({
            "id": "",
            "city": item.city,
            "count": item.count,
            "untreatedCount": item.untreatedCount,
            "processedCount": item.processedCount
        })
    return schemas.GetTroubleStatisticsResponse(data=troubles)


@router.get('/annualRiskGroup', response_model=schemas.GetTroubleStatisticsResponse)
def get_annual_risk_group():
    # srv = OrderListService(startTime=None, endTime=None, city=None, network_level='all')
    # srv.get_handled_data(['annual_statistics'], deal_all=True)
    datas = OrderListService.getAnnualRiskGroup()
    troubles = []
    for item in datas:
        troubles.append({
            "count": item.count,
            "timestamp": item.timestamp,
            "untreatedCount": item.untreatedCount,
            "processedCount": item.processedCount
        })
    return schemas.GetTroubleStatisticsResponse(data=troubles)


@router.get('/getHiddenNetworkLevel', response_model=schemas.GetTroubleStatisticsResponse)
def get_hidden_network():
    # srv = OrderListService(startTime=None, endTime=None, city=None, network_level='all')
    # srv.get_handled_data(['network_level'], deal_all=True)
    datas = OrderListService.getHiddenNetwork()
    troubles = []
    for item in datas:
        troubles.append({
            "name": item.network_level,
            "value": item.network_level
        })
    return schemas.GetTroubleStatisticsResponse(data=troubles)


@router.post("/HazardLevelCityGroup/", response_model=schemas.GetTroubleUnhandleResponse)
def get_city_risk_level_statistics(order_list_req: schemas.HazardLevelCityGroupRequest):
    # srv = OrderListService(**order_list_req.dict())
    # srv.get_handled_data(['city_statistics'])
    datas = OrderListService.getHazardLevelCityGroup(order_list_req)
    troubles = []
    result = {
        "city": "全省",
        "general_count": 0,
        "general_untreatedCount": 0,
        "general_processedCount": 0,
        "emergency_count":0,
        "emergency_untreatedCount": 0,
        "emergency_processedCount": 0
    }
    
    for item in datas:
        general_count = item.general_count
        general_untreatedCount = item.general_untreatedCount
        general_processedCount = item.general_processedCount
        emergency_count = item.emergency_count
        emergency_untreatedCount = item.emergency_untreatedCount
        emergency_processedCount = item.emergency_processedCount
        troubles.append({
            "city": item.city,
            "general_count": general_count,
            "general_untreatedCount": general_untreatedCount,
            "general_processedCount": general_processedCount,
            "emergency_count": emergency_count,
            "emergency_untreatedCount": emergency_untreatedCount,
            "emergency_processedCount": emergency_processedCount
        })
        result["general_count"] += general_count
        result['general_untreatedCount'] += general_untreatedCount
        result['general_processedCount'] += general_processedCount
        result['emergency_count'] += emergency_count
        result['emergency_untreatedCount'] += emergency_untreatedCount
        result['emergency_processedCount'] += emergency_processedCount
    result["myArray"] = troubles
    return schemas.GetTroubleUnhandleResponse(data=result)


@router.get("/getFilter",
            response_model=schemas.FilterResponse,
            summary="返回过滤条件")
def get_filter():
    order_list = get_order_list_filter()
    filter_list = []
    for item in order_list:
        filter_list.append({
            "city": item.city,
            "district_county": item.district_county,
            "sys_name": item.sys_name
        })
        # filter_list.append({
        #     "city": item.city,
        #     "district_county": item.district_county,
        #     "sys_name": item.sys_name,
        #     "network_level": item.network_level,
        #     "risk_level": item.risk_level,
        #     "is_top_end": "未派单" if item.is_top_end == 0 else "已派单",
        #     "is_send_top": "未处理" if item.is_top_end == 0 else "已处理"
        # })
    return schemas.FilterResponse(
        data=filter_list
    )


# getFilterLarterPart
@router.get("/getFilterLarterPart",
            response_model=schemas.FilterResponse,
            summary="返回剩下的过滤条件")
def get_filter_later_part():
    order_list = get_order_list_filter_later_part()
    filter_list = []
    for item in order_list:
        filter_list.append({
            "network_level": item.network_level,
            "risk_level": item.risk_level,
            "is_top_end": "未派单" if item.is_top_end == 0 else "已派单",
            "is_send_top": "未处理" if item.is_top_end == 0 else "已处理"
        })
    return schemas.FilterResponse(
        data=filter_list
    )


@router.post("/getCityFilter",
             response_model=schemas.FilterResponse,
             summary="特定city的过滤条件")
def get_city_filter(city_list: List):
    filter_list = []
    filter_cities = get_filter_citys(city_list)
    for item in filter_cities:
        filter_list.append({
            "district_county": item.district_county
        })
    return schemas.FilterResponse(
        data=filter_list
    )


@router.post("/HazardLevelDistrictGroup",
             response_model=schemas.GetTroubleUnhandleResponse,
             summary="特定city的getHazardLevelDistrictGroup数据")
def get_hazard_level_district_group(req: schemas.OrderListRequest):
    datas = OrderListService.getHazardLevelDistrictGroup(req)
    troubles = []
    result = {
        "city": req.city,
        "general_count": 0,
        "general_untreatedCount": 0,
        "general_processedCount": 0,
        "emergency_count":0,
        "emergency_untreatedCount": 0,
        "emergency_processedCount": 0
    }
    
    for item in datas:
        general_count = item.general_count
        general_untreatedCount = item.general_untreatedCount
        general_processedCount = item.general_processedCount
        emergency_count = item.emergency_count
        emergency_untreatedCount = item.emergency_untreatedCount
        emergency_processedCount = item.emergency_processedCount
        troubles.append({
            "district": item.district_county,
            "general_count": general_count,
            "general_untreatedCount": general_untreatedCount,
            "general_processedCount": general_processedCount,
            "emergency_count": emergency_count,
            "emergency_untreatedCount": emergency_untreatedCount,
            "emergency_processedCount": emergency_processedCount
        })
        result["general_count"] += general_count
        result['general_untreatedCount'] += general_untreatedCount
        result['general_processedCount'] += general_processedCount
        result['emergency_count'] += emergency_count
        result['emergency_untreatedCount'] += emergency_untreatedCount
        result['emergency_processedCount'] += emergency_processedCount
    result["myArray"] = troubles
    return schemas.GetTroubleUnhandleResponse(data=result)
