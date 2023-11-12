from ..models.check_oa_board_type import CheckOaBoardType


def get_total(filters):
    return CheckOaBoardType.get_total(0, filters=filters)


def get_by_page(page_idx, page_size, filters=None):
    check_oa_board_types = CheckOaBoardType.get_by_page_size(0, page_idx, page_size, filters)
    return set_data(check_oa_board_types)


def get_all(filters):
    check_oa_board_types = CheckOaBoardType.get_by_filter(0, filters)
    return set_data(check_oa_board_types)


def set_data(check_oa_board_types):
    return [{
        "sys_name": ct.sys_name,
        "sub_name": ct.sub_name,
        "shelf_id": ct.shelf_id,
        "slot_id": ct.slot_id,
        "board_model": ct.board_model,
        "data_error": ct.data_error
        } for ct in check_oa_board_types]
