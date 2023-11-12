from ..models.check_optical_ne import CheckOpticalNe


def get_total(filters):
    return CheckOpticalNe.get_total(0, filters=filters)


def get_by_page(page_idx, page_size, filters=None):
    check_optical_nes = CheckOpticalNe.get_by_page_size(0, page_idx, page_size, filters)
    return set_data(check_optical_nes)


def get_all(filters):
    check_optical_nes = CheckOpticalNe.get_by_filter(0, filters)
    return set_data(check_optical_nes)


def set_data(check_optical_nes):
    return [{
        "sys_name": ct.sys_name,
        "network_level": ct.network_level,
        "city": ct.city,
        "ne_name": ct.ne_name,
        "sub_name": ct.sub_name,
        "manufactor": ct.manufactor,
        "ne_type": ct.ne_type,
        "ne_model": ct.ne_model,
        "data_error": ct.data_error
        } for ct in check_optical_nes]
