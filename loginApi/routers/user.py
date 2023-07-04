from fastapi import APIRouter, status, HTTPException
from .. import schemas
from ..services import user_srv
from common.redis import redis_client, AUTH_DB, TOKEN_USER_HSET


router = APIRouter(
    prefix='/User',
    tags=['user']
)


@router.post("/getUserInfo/",
             response_model=schemas.UserInfosResponse,
             summary="返回当前系统用户信息列表")
def get_userinfo_list(req: schemas.UserInfoRequest):
    redis = redis_client(AUTH_DB)
    username = redis.hget(TOKEN_USER_HSET, req.token)
    if not username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    req_json = {}
    if req.phone and len(req.phone) > 0:
        req_json['cellphone_num'] = req.phone
    if req.state and len(req.state) > 0:
        if req.state == "1":
            req_json['is_active'] = 1
        elif req.state == "0":
            req_json['is_active'] = 0
    if req.userName and len(req.userName) > 0:
        req_json['user_name'] = req.userName
    
    users = user_srv.get_all_userinfos(**req_json)
    filter_users = list(filter(lambda usr: usr.user_name != username, users))
    return schemas.UserInfosResponse(
        data=[user.to_dict() for user in filter_users]
    )
