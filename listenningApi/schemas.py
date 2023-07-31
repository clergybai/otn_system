from pydantic import BaseModel
from fastapi import status
from common.msg import message
from datetime import datetime, timezone, timedelta


class OtnBaseResponse(BaseModel):
    code: int = status.HTTP_200_OK
    msg: str = message.REQ_SUCCESS
    response_time = datetime.now(timezone(timedelta(hours=8)))


class ComputedStateResponse(OtnBaseResponse):
    code_type: int = status.HTTP_200_OK
    data: int


class StartComputedResponse(OtnBaseResponse):
    code_type: int = status.HTTP_200_OK
    data: bool
