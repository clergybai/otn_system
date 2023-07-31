from .. import schemas
from fastapi import APIRouter
from ..services.order_list_srv import OrderListService


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
    srv = OrderListService(**order_list_req.dict())
    srv.get_handled_data([])
    return schemas.GetTroubleUnhandleResponse(data=srv.get_unhandled())


@router.post("/Statistics/", response_model=schemas.GetTroubleStatisticsResponse)
def get_statistics(order_list_req: schemas.OrderListRequest):
    srv = OrderListService(**order_list_req.dict())
    srv.get_handled_data(['statistics'])
    return schemas.GetTroubleStatisticsResponse(data=srv.get_statistics())


@router.post("/level/", response_model=schemas.GetTroubleStatisticsResponse)
def get_network_level(order_list_req: schemas.OrderListRequest):
    srv = OrderListService(**order_list_req.dict())
    srv.get_handled_data(['network_level'])
    return schemas.GetTroubleStatisticsResponse(data=srv.get_network_level())


@router.get("/cityHiddenGroup", response_model=schemas.GetTroubleStatisticsResponse)
def get_city_hidden_group():
    srv = OrderListService(startTime=None, endTime=None, city=None, network_level='all')
    srv.get_handled_data(['city_group'])
    return schemas.GetTroubleStatisticsResponse(data=srv.get_city_statistics())


@router.get('/annualRiskGroup', response_model=schemas.GetTroubleStatisticsResponse)
def get_annual_risk_group():
    srv = OrderListService(startTime=None, endTime=None, city=None, network_level='all')
    srv.get_handled_data(['annual_statistics'], deal_all=True)
    return schemas.GetTroubleStatisticsResponse(data=srv.get_annual_statistics())


@router.get('/getHiddenNetwork', response_model=schemas.GetTroubleStatisticsResponse)
def get_hidden_network():
    srv = OrderListService(startTime=None, endTime=None, city=None, network_level='all')
    srv.get_handled_data(['network_level'], deal_all=True)
    return schemas.GetTroubleStatisticsResponse(data=srv.get_hidden_network_level())


@router.post("/HazardLevelCityGroup/", response_model=schemas.GetTroubleStatisticsResponse)
def get_city_risk_level_statistics(order_list_req: schemas.OrderListRequest):
    srv = OrderListService(**order_list_req.dict())
    srv.get_handled_data(['city_statistics'])
    return schemas.GetTroubleStatisticsResponse(data=srv.get_city_risk_level_statistics())
