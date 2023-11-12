from typing import List, Optional
from pydantic import BaseModel
from fastapi import status
from common.msg import message
from datetime import datetime, timezone, timedelta


class OtnBaseResponse(BaseModel):
    code: int = status.HTTP_200_OK
    msg: str = message.REQ_SUCCESS
    response_time = datetime.now(timezone(timedelta(hours=8)))


class FilterResponse(OtnBaseResponse):
    data: List[dict]


class BoardItem(BaseModel):
    is_calculating: bool
    myArray: List[dict]
    page_count: int
    page_index_begin: int
    page_size: int
    total: int


class CheckTopologyItem(BaseModel):
    myArray: List[dict]
    page_count: int
    page_index_begin: int
    page_size: int
    total: int


class GetBoardResponse(OtnBaseResponse):
    code_type: int = status.HTTP_200_OK
    data: Optional[BoardItem] = None


class GetCheckTopologyResponse(OtnBaseResponse):
    code_type: int = status.HTTP_200_OK
    data: Optional[CheckTopologyItem] = None


class UploadFileResponse(OtnBaseResponse):
    code_type: int = status.HTTP_200_OK
    data: Optional[str] = None


class AddOaBoardStandardRequest(BaseModel):
    board_model: str
    standard_gain_max: str
    standard_gain_min: str
    standard_single_40_wave_output: str
    standard_single_80_wave_output: str
    standard_single_96_wave_output: str


class AddOaBoardStandardResponse(OtnBaseResponse):
    code_type: int = status.HTTP_200_OK
    data: object = None


class GetBoardRequest(BaseModel):
    page_index_begin: int
    page_size: int
    filter: Optional[List[dict]]


class ExportRequest(BaseModel):
    filter: Optional[List[dict]] = None


class StdValueItem(BaseModel):
    optical_power_baseline: int
    gain_baseline: int
    olp_act_stand_baseline: int
    cable_in_out_baseline: int


class GetDefaultStdValueResponse(OtnBaseResponse):
    code_type: int = status.HTTP_200_OK
    data: StdValueItem


class GetDefaultThreadResponse(OtnBaseResponse):
    code_type: int = status.HTTP_200_OK
    data: dict


class GetRuleWithNameResponse(OtnBaseResponse):
    code_type: int
    data: object = None


class GetRuleWithNameRequest(BaseModel):
    rule_name: str


class ParamItem(BaseModel):
    selected: List[str]


class MslGetRequest(BaseModel):
    filter: Optional[List[dict]] = None
    page_index_begin: int
    page_size: int
    param: ParamItem


class MslEditRequest(BaseModel):
    a_ne_id: str
    a_sub_name: str
    business_waves: int
    city: str
    net_level: str
    sys_name: str
    z_ne_id: str
    z_sub_name: str
