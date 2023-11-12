from ..models.input_pm_mca import InputPmMca


def get_pm_mca(brand):
    pm_mcas = InputPmMca.get(100, manufactor=brand)
    rtn = []
    for item in pm_mcas:
        rtn.append({
            "sub_name": item.sub_name,
            "brd_name": item.brd_name,
            "shelf_id": item.shelf_id,
            "slot_id": item.slot_id,
            "port_id": item.port_id,
            "path_id": item.path_id,
            "direction": item.direction,
            "och_power": item.och_power
        })
    return rtn
