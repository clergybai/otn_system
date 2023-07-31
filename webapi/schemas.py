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
    startTime: Optional[datetime] = None
    endTime: Optional[datetime] = None
    city: Optional[str] = None
    network_level: Optional[str] = None


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


class DrawTopoData(BaseModel):
    nodes: List[dict]
    edges: List[dict]
    system_details: dict
    id: Optional[str] = None


class DrawTopoResponse(GetTroubleBaseResponse):
    data: DrawTopoData


class BoardItem(BaseModel):
    myArray: List[dict]
    page_count: int
    page_index_begin: int
    page_size: int
    total: int
    is_calculating: bool


class GetTroubleResponse(GetTroubleBaseResponse):
    data: BoardItem
