from ..models.input_oms_business_waves import InputOmsBusinessWaves
from ..models.calc_oms import CalcOms
from ..models.calc_ne_adj import CalcNeAdj
from listenningApi.models.input_topology_data import InputTopologyData


def get_msl_by_filter(**kwargs):
    total, items = InputOmsBusinessWaves.get_oms_by_filter(**kwargs)
    return total, [{
        "sys_name": item.sys_name,
        "city": item.city,
        "net_level": item.net_level,
        "a_sub_name": item.a_sub_name,
        "a_ne_id": item.a_ne_id,
        "z_sub_name": item.z_sub_name,
        "z_ne_id": item.z_ne_id,
        "business_waves": item.business_waves
    } for item in items]


def get_is_history_count_in_0_2():
    return InputOmsBusinessWaves.get_count(is_history=[0, 2])


def get_count_by_calc_oms_join_input_oms_business_waves():
    sql_str = """SELECT count(*) FROM `calc_oms` AS OMS LEFT JOIN `input_oms_business_waves` as INPUT 
    ON OMS.`sys_name` = INPUT.`sys_name` AND OMS.`oms_source_id` = INPUT.`a_ne_id` AND OMS.`oms_target_id` = INPUT.`z_ne_id` AND OMS.`is_history` = 0 AND OMS.`is_history` = INPUT.`is_history` 
    WHERE OMS.`timestamp` > INPUT.`timestamp`;"""
    return InputOmsBusinessWaves.execute_raw_sql(sql_str)


def check_update_timestamp() -> bool:
    count = get_is_history_count_in_0_2()
    if count == 0:
        return True
    count = get_count_by_calc_oms_join_input_oms_business_waves()
    return count > 0


def delete_history_one():
    return InputOmsBusinessWaves.delete(is_history=1)


def move_history_zero_to_one():
    filters = {}
    filters['is_history'] = 0
    return InputOmsBusinessWaves.update(filters, is_history=1)


def copy_running_data_for_update():
    oms = CalcOms.get(is_history=0)
    input_topology_datas = InputTopologyData.get(is_history=0)
    input_oms_businesses = []
    for om in oms:
        sys_name = om.sys_name
        oms_source_id = om.oms_source_id
        net_level = ""
        city = ""
        topology_find = find_input_oms_biz(input_topology_datas, om)
        if topology_find:
            net_level = topology_find.net_level
            city = topology_find.city
        input_oms_businesses.append(InputOmsBusinessWaves(
            sys_name=sys_name,
            net_level=net_level,
            city=city,
            a_ne_id=oms_source_id,
            z_ne_id=om.oms_target_id,
            business_waves=om.business_waves,
            is_history=0,
        ))
    if len(input_oms_businesses) > 0:
        InputOmsBusinessWaves.add_input_oms_bizs(input_oms_businesses)


def find_input_oms_biz(input_oms_businesses, om):
    sys_name = om.sys_name
    oms_source_id = om.oms_source_id
    for biz in input_oms_businesses:
        if (biz.a_ne_id == oms_source_id or biz.z_ne_id == oms_source_id) and biz.sys_name == sys_name:
            return biz
    return None


def find_ne_from_calc_ne_adjs(calc_s, oms, is_a):
    ne_id = oms.a_ne_id if is_a else oms.z_ne_id
    for cal in calc_s:
        if cal.source_ne_id == ne_id or cal.target_ne_id == ne_id:
            return cal
    return None


def update_node_names():
    data = InputOmsBusinessWaves.get_oms_by_filter(is_history=0)
    calc_s = CalcNeAdj.get(is_history=0)
    
    update_mappings = []
    
    for item in data:
        a_sub_name = ""
        z_sub_name = ""
        find_a = find_ne_from_calc_ne_adjs(calc_s, item, True)
        find_z = find_ne_from_calc_ne_adjs(calc_s, item, False)
        if find_a:
            a_sub_name = find_a.source_sub_name if find_a.source_sub_name == item.a_ne_id else find_a.target_sub_name
        if find_z:
            z_sub_name = find_z.source_sub_name if find_z.source_ne_id == item.z_ne_id else find_z.target_sub_name
        update_mappings.append({
            "id": item.id,
            "a_sub_name": a_sub_name,
            "z_sub_name": z_sub_name
        })
    if len(update_mappings) > 0:
        InputOmsBusinessWaves.bulk_update(update_mappings=update_mappings)    


def update():
    if not check_update_timestamp():
        return
    # DeleteHistoryOne();
    delete_history_one()
    # MoveHistoryZeroToOne();
    move_history_zero_to_one()
    # CopyRunningDataForUpdate();
    copy_running_data_for_update()
    # UpdateNodeNames();
    update_node_names()


def update_wave(req):
    filters = {}
    filters["sys_name"] = req.sys_name
    filters["a_sub_name"] = req.a_sub_name
    filters["a_ne_id"] = req.a_ne_id
    filters["z_sub_name"] = req.z_sub_name
    filters["z_ne_id"] = req.z_ne_id
    InputOmsBusinessWaves.update(filters=filters, business_waves=req.business_waves)
    

def check_request(req) -> bool:
    if req is None:
        return False
    if not req.sys_name or len(req.sys_name) == 0:
        return False
    if not req.a_ne_id or len(req.a_ne_id) == 0:
        return False
    if not req.a_sub_name or len(req.a_sub_name) == 0:
        return False
    if not req.z_ne_id or len(req.z_ne_id) == 0:
        return False
    if not req.business_waves or req.business_waves < 0 or req.business_waves > 100:
        return False
    return True
