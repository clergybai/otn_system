from ..models.user_perms import UserPerms
from ..models.front_city_permission import FrontCityPermission
import json


def get_user_perms(user_name):
    return UserPerms.get_by(user_name=user_name)


def convert_user_perm_to_dict(user_perm):
    print(f"user_perm: {str(user_perm)}")
    return {
        "can_add_standrad_param": user_perm.can_add_standrad_param == 1,
        "can_modify_base_line": user_perm.can_modify_base_line == 1,
        "can_threshold_setting": user_perm.can_threshold_setting == 1,
        "can_add_user": user_perm.can_add_user == 1,
        "can_modify_prems": user_perm.can_modify_prems == 1,
        "can_output_hiddentrouble": user_perm.can_output_hiddentrouble == 1,
        "can_save_topo_position": user_perm.can_save_topo_position == 1,
        "can_set_channel_num": user_perm.can_set_channel_num == 1
    }


def get_all_user_perms():
    return UserPerms.get_all_user_perms()


def upsert_user_perm(**kwargs):
    user_name = kwargs.pop('user_name')
    user_perm = UserPerms.get_by(user_name=user_name)
    if user_perm:
        return UserPerms.update(user_name=user_name, **kwargs)
    else:
        kwargs['user_name'] = user_name
        UserPerms.add_new_user_perm(**kwargs)
        return True


def get_menu_by_user(username):
    perm_list = FrontCityPermission.get(is_history=0)
    user_perm = UserPerms.get_by(user_name=username)
    if user_perm is None:
        return None
    zones = json.loads(user_perm.zone_authen)
    for item in zones:
        infos = []
        if "二干" in item["name"]:
            front_eg = [find for find in perm_list if find.net_level == item["name"] and find.sys_name != ""]
            front_eg = set([it.sys_name for it in front_eg]) # list(set(front_eg))
            for index, front_item in enumerate(front_eg):
                infos.append({
                    "name": front_item,
                    "code": front_item + "-" + str(index),
                    "type": 0,
                    "children": item['children'],
                    "IsAuthentication": True
                })
        else:
            front_ct = [find for find in perm_list if find.city == item["name"] and find.sys_name != "" and "二干" not in find.net_level]
            front_ct = set([it.sys_name for it in front_ct])# list(set(front_ct))
            for index, front_item in enumerate(front_ct):
                infos.append({
                    "name": front_item,
                    "code": front_item + "-" + str(index),
                    "type": 0,
                    "children": item['children'],
                    "IsAuthentication": True
                })
        val = next((find for find in zones if find["name"] == item["name"]), None)
        if val:
            val["children"] = sorted(infos, key=lambda x: x["name"])
    return zones
