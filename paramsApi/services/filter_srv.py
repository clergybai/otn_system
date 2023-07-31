from ..models.input_oa_board_standard import InputOaBoardStandard
from ..models.input_oa_board_type import InputOaBoardType
from ..models.input_voa_config import InputVoaConfig


def get_all_filters():
    boards = InputOaBoardStandard.get_input_oa_board_standards()
    return [{"board_model": bd.board_model} for bd in boards]


def get_board_by_page(page_idx, page_size, filters=None):
    boards = InputOaBoardStandard.get_board_by_page_size(11, page_idx, page_size, filters)
    return [{
        "board_model": bd.board_model,
        "standard_gain_min": bd.standard_gain_min,
        "standard_gain_max": bd.standard_gain_max,
        "standard_single_40_wave_output": bd.standard_single_40_wave_output,
        "standard_single_80_wave_output": bd.standard_single_80_wave_output,
        "standard_single_96_wave_output": bd.standard_single_96_wave_output if bd.standard_single_96_wave_output else 0
        } for bd in boards]


def get_board_type_by_page(page_idx, page_size, filters=None):
    types = InputOaBoardType.get_board_types_by_page_size(11, page_idx, page_size, filters)
    return [{
        "sub_name": tp.sub_name,
        "shelf_id": tp.shelf_id,
        "slot_id": tp.slot_id,
        "board_model": tp.board_model
        } for tp in types]


def get_voa_config_by_page(page_idx, page_size, filters=None):
    configs = InputVoaConfig.get_voa_configs_by_page_size(11, page_idx, page_size, filters)
    return [{
        "sub_name": cfg.sub_name,
        "shelf_id": cfg.shelf_id,
        "slot_id": cfg.slot_id,
        "port_id": cfg.port_id,
        "voa_vaule": cfg.voa_vaule
        } for cfg in configs]


def get_board_total(filters):
    return InputOaBoardStandard.get_board_total(11, filters=filters)


def get_board_type_total(filters):
    return InputOaBoardType.get_board_types_total(11, filters=filters)


def get_voa_config_total(filters):
    return InputVoaConfig.get_voa_configs_total(11, filters=filters)


def add_board_info(info):
    if len(info['board_model']) == 0:
        return False
    standard_gain_max = int(info['standard_gain_max'])
    if standard_gain_max < 5 or standard_gain_max > 40:
        return False
    standard_gain_min = int(info['standard_gain_min'])
    if standard_gain_min < 5 or standard_gain_min > 40:
        return False
    if standard_gain_min > standard_gain_max:
        return False
    standard_single_40_wave_output = int(info['standard_single_40_wave_output'])
    if standard_single_40_wave_output < -5 or standard_single_40_wave_output > 15:
        return False
    standard_single_80_wave_output = int(info['standard_single_80_wave_output'])
    if standard_single_80_wave_output < -10 or standard_single_80_wave_output > 15:
        return False
    # special treat
    if info['standard_single_96_wave_output']:
        standard_single_96_wave_output = int(info['standard_single_96_wave_output'])
    else:
        standard_single_96_wave_output = None

    InputOaBoardStandard.add(
        board_model=info['board_model'],
        standard_gain_max=standard_gain_max,
        standard_gain_min=standard_gain_min,
        standard_single_40_wave_output=standard_single_40_wave_output,
        standard_single_80_wave_output=standard_single_80_wave_output,
        standard_single_96_wave_output=standard_single_96_wave_output)
    return True
