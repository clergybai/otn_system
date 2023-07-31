from fastapi import APIRouter, status, HTTPException
from .. import schemas
from ..services import user_srv, permissions_srv
from datetime import datetime
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


@router.post("/addUser/",
             response_model=schemas.AddUserResponse,
             summary="添加新用户")
def add_user(req: schemas.UserRequest):
    user = user_srv.get_all_userinfos(user_name=req.user_name)
    if len(user) != 0:
        return schemas.AddUserResponse(
            data=-1
        )
    # add to user table
    user_srv.add_user(req.dict())
    # add to user perms
    user_perms_dict = {}
    user_perms_dict['user_name'] = req.user_name
    user_perms_dict['zone_authen'] = '[]'
    user_perms_dict['can_add_standrad_param'] = 0
    user_perms_dict['can_modify_base_line'] = 0
    user_perms_dict['can_threshold_setting'] = 0
    user_perms_dict['can_add_user'] = 0
    user_perms_dict['can_modify_prems'] = 0
    user_perms_dict['can_output_hiddentrouble'] = 0
    user_perms_dict['can_save_topo_position'] = 0
    user_perms_dict['can_set_channel_num'] = 0
    user_perms_dict['create_time'] = datetime.now()
    user_perms_dict['last_update_person'] = req.last_update_person
    permissions_srv.upsert_user_perm(**user_perms_dict)
    return schemas.AddUserResponse(
        data=1
    )


@router.post("/removeUser/",
             response_model=schemas.RemoveUserResponse,
             summary="删除用户")
def remove_user(req: schemas.UserRequest):
    return schemas.RemoveUserResponse(
        data=user_srv.remove_user(req.dict())
    )


@router.post("/editUser/",
             response_model=schemas.RemoveUserResponse,
             summary="编辑用户信息")
def edit_user(req: schemas.UserRequest):
    return schemas.RemoveUserResponse(
        data=user_srv.edit_user(req.dict())
    )


@router.post("/updatePwd/",
             response_model=schemas.RemoveUserResponse,
             summary="用户登录密码更新")
def update_pwd(req: schemas.PwdUpdateRequest):
    return schemas.RemoveUserResponse(
        data=user_srv.pwd_update(req.dict())
    )
