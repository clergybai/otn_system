from typing import List, Optional
from pydantic import BaseModel, EmailStr
from fastapi import status
from common.msg import message
from datetime import datetime, timezone, timedelta


class GetMenuRequest(BaseModel):
    username: str


class KeyRequest(BaseModel):
    addr: str
    public_key: Optional[str] = None
    is_test: Optional[bool] = None


class KeyDataResponse(BaseModel):
    addr: str
    public_key: str


class OtnBaseResponse(BaseModel):
    code: int = status.HTTP_200_OK
    msg: str = message.REQ_SUCCESS
    response_time = datetime.now(timezone(timedelta(hours=8)))


class UserPermsResponse(OtnBaseResponse):
    data: List[dict]


class SetLogResponse(OtnBaseResponse):
    code_type: int = status.HTTP_200_OK
    data: bool


class SetLogRequest(BaseModel):
    op_behavior: str
    op_module: str
    op_time: datetime
    op_user: str


class KeyResponse(OtnBaseResponse):
    data: KeyDataResponse


class LoginRequest(BaseModel):
    user_name: str
    mac_addr: str
    pw_word: str
    token: str = ""
    is_test: Optional[bool] = None


class LoginDataResponse(BaseModel):
    token: str
    user_name: str
    is_authen: dict


class LoginResponse(OtnBaseResponse):
    data: LoginDataResponse


class UserInfoRequest(BaseModel):
    phone: Optional[str] = None
    state: Optional[str] = None
    token: str
    userName: Optional[str] = None


class UserInfosResponse(OtnBaseResponse):
    data: List[dict]


class LogRequest(BaseModel):
    startTime: str = ""
    endTime: str = ""
    op_user: Optional[str] = None


class DataListResponse(OtnBaseResponse):
    code_type: int = status.HTTP_200_OK
    data: List[dict]


class UpdateResponse(OtnBaseResponse):
    code_type: int = status.HTTP_200_OK
    data: bool


class UserRequest(BaseModel):
    cellphone_num: str
    city: str
    create_time: str
    department: str
    is_active: str
    last_update_person: str
    name: str
    post: str
    remark: str
    role: str
    salt: Optional[str] = None
    update_time: str
    user_email: EmailStr
    user_name: str


class PwdUpdateRequest(BaseModel):
    userName: str
    salt: str
    resalt: str


class AddUserResponse(OtnBaseResponse):
    data: int


class RemoveUserResponse(OtnBaseResponse):
    code_type: int = status.HTTP_200_OK
    data: bool
