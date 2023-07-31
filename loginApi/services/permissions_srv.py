from ..models.user_perms import UserPerms


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
