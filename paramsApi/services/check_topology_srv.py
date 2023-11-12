from ..models.check_topology import CheckTopology


def get_total(filters):
    return CheckTopology.get_total(0, filters=filters)


def get_by_page(page_idx, page_size, filters=None):
    check_topologies = CheckTopology.get_by_page_size(0, page_idx, page_size, filters)
    return set_data(check_topologies)


def get_all(filters):
    check_topologies = CheckTopology.get_by_filter(0, filters)
    return set_data(check_topologies)


def set_data(check_topologies):
    return [{
        "sys_name": ct.sys_name,
        "net_level": ct.net_level,
        "city": ct.city,
        "a_sub_name": ct.a_sub_name,
        "a_shelf_id": ct.a_shelf_id,
        "a_slot_id": ct.a_slot_id,
        "a_in_out_id": ct.a_in_out_id,
        "z_sub_name": ct.z_sub_name,
        "z_shelf_id": ct.z_shelf_id,
        "z_slot_id": ct.z_slot_id,
        "z_in_out_id": ct.z_in_out_id,
        "full_waves": ct.full_waves,
        "fiber_length": ct.fiber_length,
        "data_error": ct.data_error
        } for ct in check_topologies]
