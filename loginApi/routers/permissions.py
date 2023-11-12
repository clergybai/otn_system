from fastapi import APIRouter
from ..services.permissions_srv import (get_user_perms, get_all_user_perms,
                                        upsert_user_perm, get_menu_by_user)
from ..services.front_city_permission_srv import get_city_permissions, get_all_cities
from .. import schemas
from common.consts import db_consts
import json

router = APIRouter(
    prefix='/Permissions',
    tags=['Permissions']
)


def gen_city_permission_list(city_permissions):
    rtn = []
    idx = 0
    for item in city_permissions:
        rtn.append({
            "name": item[0],
            "code": f"{item[0]}_{idx}",
            "type": 0,
            "children": [],
            "IsAuthentication": True
        })
        idx = idx+1
    return rtn


@router.post("/getMenu/",
             response_model=schemas.UserPermsResponse,
             summary="返回属于该用户的基于zone_authen的sys_name")
def get_menu(req: schemas.GetMenuRequest):
    # usr_perms = get_user_perms(user_name=req.username)
    # zone_authens = json.loads(usr_perms.zone_authen)
    # has_net_level = False
    # net_level_fields = ['sys_name', 'net_level']
    # city_fields = ['sys_name', 'city']
    # city_list = []
    # for zone in zone_authens:
    #     if zone['name'] == db_consts.NET_LEVEL:
    #         has_net_level = True
    #     else:
    #         city_list.append(zone['name'])

    # data = []
    # if has_net_level:
    #     er_gan_nets = get_city_permissions('sys_name', net_level_fields, net_level=db_consts.NET_LEVEL, is_history=0)
    #     data.append({
    #         "name": db_consts.NET_LEVEL,
    #         "code": None,
    #         "type": 0,
    #         "children": gen_city_permission_list(er_gan_nets),
    #         "IsAuthentication": True
    #     })

    # city_sys_name_list = get_city_permissions('sys_name', city_fields, city=city_list, is_history=0)
    # temp_dict = {}
    # for city_sys in city_sys_name_list:
    #     if temp_dict.get(city_sys[1]):
    #         temp_dict[city_sys[1]].add(city_sys)
    #     else:
    #         temp_dict[city_sys[1]] = {city_sys}

    # for key, val in temp_dict.items():
    #     data.append({
    #         "name": key,
    #         "code": None,
    #         "type": 0,
    #         "children": gen_city_permission_list(list(val)),
    #         "IsAuthentication": True
    #     })
    return schemas.UserPermsResponse(data=get_menu_by_user(req.username))


@router.get("/getPerm/",
            response_model=schemas.DataListResponse,
            summary="get user permission list")
def get_user_perm_list():
    perms = get_all_user_perms()
    return schemas.DataListResponse(
        data=[perm.to_dict() for perm in perms]
    )


@router.get("/getCity",
            response_model=schemas.DataListResponse,
            summary="get all city list")
def get_cities():
    cities = ['二干/省内骨干网']
    cities.extend(get_all_cities())
    # 去除city是空字符串
    cities = [s for s in cities if s]
    print(f"cities: {str(cities)}")
    return schemas.DataListResponse(
        data=[{
            "name": city,
            "code": "---",
            "type": 0,
            "children": [],
            "IsAuthentication": True
        } for city in cities]
    )


@router.post("/setPermission/",
             response_model=schemas.UpdateResponse,
             summary="Update user permission")
def set_permission(req: dict):
    req.pop('zone_authenArr')
    return schemas.UpdateResponse(
        data=upsert_user_perm(**req)
    )
