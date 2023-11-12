from typing import List, Optional
from pydantic import BaseModel
from fastapi import status
from common.msg import message
from datetime import datetime, timezone, timedelta


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


class OrderListRequest(BaseModel):
    startTime: Optional[str] = ""
    endTime: Optional[str] = ""
    city: Optional[str] = None
    network_level: Optional[str] = None


class HazardLevelCityGroupRequest(BaseModel):
    selected: List[str]
    timesArr: OrderListRequest


class GetTroubleBaseResponse(BaseModel):
    code: int = status.HTTP_200_OK
    msg: str = message.REQ_SUCCESS
    response_time = datetime.now(timezone(timedelta(hours=8)))


class GetTroubleUnhandleResponse(GetTroubleBaseResponse):
    data: dict


class GetTroubleStatisticsResponse(GetTroubleBaseResponse):
    data: List[dict]


class FilterItem(BaseModel):
    name: Optional[str] = None
    values: Optional[List[str]] = None


class TimesArrItem(BaseModel):
    startTime: str = ""
    endTime: str = ""


class ParamField(BaseModel):
    timesArr: TimesArrItem
    order_id: str = ""
    selected: List[str]


class TroubleSearchRequest(BaseModel):
    page_index_begin: int = 0
    page_size: int = 20
    filter: List[FilterItem]
    param: ParamField


class DrawTopoRequest(BaseModel):
    code: str
    perms: bool
    sys_name: str
    user_name: str


class MainSiteDetailRequest(BaseModel):
    self: str
    sys_name: str


# 2023-09-01
class OaDetailsRequest(BaseModel):
    oa_fingerpring: str


# 2023-09-02
class FiberDetailsRequest(BaseModel):
    act_stand: str
    source_ne_id: str
    target_ne_id: str


class DrawTopoData(BaseModel):
    nodes: List[dict]
    edges: List[dict]
    system_details: Optional[dict] = None
    id: Optional[str] = None


class MainSiteDetailData(BaseModel):
    is_olp: int = 0
    mainFingerprint: List[dict]
    manufactor_type_model: str
    sub_name: str
    sub_nameArr: List[dict]
    type: str


# 2023-08-31
class OlaDetailData(BaseModel):
    id: Optional[str] = None
    ne_id: Optional[str] = None
    sub_name: Optional[str] = None
    source_sub_name: Optional[str] = None
    target_sub_name: Optional[str] = None
    source_oa_fingerprintArr: List[dict] = None
    target_oa_fingerprintArr: List[dict] = None


# 2023-09-01
class OaDetailsData(BaseModel):
    brd_type: Optional[str] = None
    gain: Optional[float] = None
    id: Optional[str] = None
    in_ne_subname: Optional[str] = None
    input_power: Optional[float] = None
    input_stand_power: Optional[float] = None
    inside_voa: Optional[float] = None
    is_history: int
    ishigh: Optional[dict] = None
    ne_id: Optional[str] = None
    ne_incoming_power: Optional[float] = None
    ne_outing_power: Optional[int] = None
    oa_risk_num: Optional[int] = None
    oms: Optional[str] = None
    out_ne_subname: Optional[str] = None
    output_power: Optional[float] = None
    output_stand_power: Optional[float] = None
    outside_voa: Optional[float] = None
    pre_position_Voa: Optional[bool] = None
    shelf_id: Optional[str] = None
    slot_id: Optional[str] = None
    stand_gain_max: Optional[int] = None
    stand_gain_min: Optional[int] = None
    timestamp: Optional[str] = None
    wavs: Optional[int] = None


# 2023-09-02
class FiberDetailsData(BaseModel):
    id: Optional[str] = None
    source_ne_id: Optional[str] = None
    target_ne_id: Optional[str] = None
    act_stand: Optional[str] = None
    source_sub_name: Optional[str] = None
    target_sub_name: Optional[str] = None
    fiber_name: Optional[str] = None
    fiber_length: Optional[int] = None
    stand_fiber_loss: Optional[float] = None
    source_out_fiber_loss: Optional[float] = None
    source_in_fiber_loss: Optional[float] = None
    source_outing_power: Optional[float] = None
    source_out_shelf_slot: Optional[str] = None
    source_incoming_power: Optional[float] = None
    source_in_shelf_slot: Optional[str] = None
    target_outing_power: Optional[float] = None
    target_out_shelf_slot: Optional[str] = None
    target_incoming_power: Optional[float] = None
    target_in_shelf_slot: Optional[str] = None
    is_risk: Optional[str] = None
    timestamp: Optional[str] = None
    is_history: Optional[int] = None
    atoz_Theory_Diff: Optional[float] = None
    ztoa_Theory_Diff: Optional[float] = None
    bothway_Diff: Optional[float] = None


class DrawTopoResponse(GetTroubleBaseResponse):
    data: DrawTopoData


class MainSiteDetailResponse(GetTroubleBaseResponse):
    data: MainSiteDetailData


# 2023-08-31
class OlaDetailResponse(GetTroubleBaseResponse):
    data: OlaDetailData


# 2023-09-01
class OaDetailsResponse(GetTroubleBaseResponse):
    data: Optional[OaDetailsData] = None


# 2023-09-02
class FiberDetailsResponse(GetTroubleBaseResponse):
    data: Optional[FiberDetailsData] = None


class BoardItem(BaseModel):
    myArray: List[dict]
    page_count: int
    page_index_begin: int
    page_size: int
    total: int
    is_calculating: bool


class GetTroubleResponse(GetTroubleBaseResponse):
    data: BoardItem


class OtnBaseResponse(BaseModel):
    code: int = status.HTTP_200_OK
    msg: str = message.REQ_SUCCESS
    response_time = datetime.now(timezone(timedelta(hours=8)))


class FilterResponse(OtnBaseResponse):
    data: List[dict]


class PositionRequest(BaseModel):
    canvasx: float
    canvasy: int
    clientx: int
    clienty: int
    ne_id: str
    sys_name: str
    user_name: str
    x: float
    y: float
