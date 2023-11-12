from .. import schemas
from fastapi import APIRouter, status
from ..services.topo_srv import (topo_draw, get_main_site_detail, get_ola_details,
                                 get_oa_details, get_fiber_details, set_position)

router = APIRouter(
    prefix='/DrawTopo',
    tags=['Draw Topo']
)


@router.post('/draw/',
             response_model=schemas.DrawTopoResponse,
             summary='获得绘制拓扑图需要的数据')
def get_draw(req: schemas.DrawTopoRequest):
    
    # get front_adj list by sys_name and is_history = 0
    nodes, edges, system_label = topo_draw(req)
    return schemas.DrawTopoResponse(
        data=schemas.DrawTopoData(
            nodes=[node.to_dict() for node in nodes],
            edges=[edge.to_dict() for edge in edges],
            system_details=system_label.to_dict() if system_label else None,
            id=None
        )
    )


@router.post('/getMainSiteDetail/',
             response_model=schemas.MainSiteDetailResponse,
             summary="获取MainSiteDetail信息"
             )
def post_main_site_detail(req: schemas.MainSiteDetailRequest):
    return schemas.MainSiteDetailResponse(
        data=get_main_site_detail(req=req)
    )


@router.post('/getOlaDetails/',
             response_model=schemas.OlaDetailResponse,
             summary="获取OlaDetail信息"
             )
def post_ola_detail(req: schemas.MainSiteDetailRequest):
    return schemas.OlaDetailResponse(
        data=get_ola_details(req)
    )


@router.post('/getOaDetails/',
             response_model=schemas.OaDetailsResponse,
             summary="获取OaDetails信息"
             )
def post_oa_details(req: schemas.OaDetailsRequest):
    return schemas.OaDetailsResponse(
        data=get_oa_details(req)
    )


@router.post('/getFiberDetails/',
             response_model=schemas.FiberDetailsResponse,
             summary="获取FiberDetails信息"
             )
def post_fiber_details(req: schemas.FiberDetailsRequest):
    return schemas.FiberDetailsResponse(
        data=get_fiber_details(req)
    )


@router.post('/position/',
             summary="position接口")
def position(req: schemas.PositionRequest):
    set_position(req)
    return status.HTTP_200_OK
