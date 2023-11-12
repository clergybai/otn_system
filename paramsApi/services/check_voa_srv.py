from ..models.check_voa import CheckVoa


def get_total(filters):
    return CheckVoa.get_total(0, filters=filters)


def get_by_page(page_idx, page_size, filters=None):
    check_voas = CheckVoa.get_by_page_size(0, page_idx, page_size, filters)
    return set_data(check_voas)


def get_all(filters):
    check_topologies = CheckVoa.get_by_filter(0, filters)
    return set_data(check_topologies)


def set_data(check_voas):
    return [{
        "sys_name": ct.sys_name,
        "sub_name": ct.sub_name,
        "shelf_id": ct.shelf_id,
        "slot_id": ct.slot_id,
        "va4_shelf_id": ct.va4_shelf_id,
        "va4_slot_id": ct.va4_slot_id,
        "va4_port_id": ct.va4_port_id,
        "data_error": ct.data_error
        } for ct in check_voas]
