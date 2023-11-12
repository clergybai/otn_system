from ..models.check_pm import CheckPm


def get_total(filters):
    return CheckPm.get_total(0, filters=filters)


def get_by_page(page_idx, page_size, filters=None):
    check_pms = CheckPm.get_by_page_size(0, page_idx, page_size, filters)
    return set_data(check_pms)


def get_all(filters):
    check_pms = CheckPm.get_by_filter(0, filters)
    return set_data(check_pms)


def set_data(check_pms):
    return [{
        "sys_name": ct.sys_name,
        "sub_name": ct.sub_name,
        "shelf_id": ct.shelf_id,
        "slot_id": ct.slot_id,
        "out_power": ct.out_power,
        "in_power": ct.in_power,
        "data_error": ct.data_error
        } for ct in check_pms]
