from ..models.front_adj import FrontAdj
from ..models.system_label import SystemLabel
from ..models.topo_ne_position import TopoNePosition
from listenningApi.models.front_picture_otm import FrontPictureOtm
from listenningApi.models.front_ne import FrontNe
from listenningApi.models.calc_ne_oas import CalcNeOas
from listenningApi.models.front_picture_ola import FrontPictureOla
from listenningApi.models.calc_oa_power import CalcOaPower
from listenningApi.models.front_data_oa import FrontDataOa
from listenningApi.models.risk_oa import RiskOa
from listenningApi.models.front_data_fiber import FrontDataFiber
from paramsApi.models.calc_oms import CalcOms


class NodeInfo(object):

    def __init__(self, id, id_str=None, nodeName=None, sys_name=None, label=None,
                 isHigh=None, act_stand=None, nodeTypeStr=None, type=None, img=None,
                 x=0, y=0, canvasx=0, canvasy=0, clientx=0, clienty=0,
                 manufactor=None, a_ne_index_id=None, z_ne_index_id=None,
                 a_ne_name=None, z_ne_name=None, ocable_length=None):
        self.id = id
        self.id_str = id_str
        self.nodeName = nodeName
        self.sys_name = sys_name
        self.label = label
        self.isHigh = isHigh
        self.act_stand = act_stand
        self.nodeTypeStr = nodeTypeStr
        self.type = type
        self.img = img
        self.x = x
        self.y = y
        self.canvasx = canvasx
        self.canvasy = canvasy
        self.clientx = clientx
        self.clienty = clienty
        self.manufactor = manufactor
        self.a_ne_index_id = a_ne_index_id
        self.z_ne_index_id = z_ne_index_id
        self.a_ne_name = a_ne_name
        self.z_ne_name = z_ne_name
        self.ocable_length = ocable_length

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def get_type(self):
        if not self.nodeTypeStr:
            return 0
        else:
            lc_nodeTypeStr = self.nodeTypeStr.lower()
            if lc_nodeTypeStr.find('otm') >= 0 or lc_nodeTypeStr.find('oadm') >= 0:
                return 1
            elif lc_nodeTypeStr.find('ola') >= 0:
                return 2
            else:
                return 0

    def get_size(self):
        type_num = self.get_type()
        if type_num == 1:
            return [100, 100]
        elif type_num == 2:
            return [60, 60]
        elif type_num == 4:
            return [700, 700]
        else:
            return None

    def to_dict(self):
        return {
            "id": self.id,
            "id_str": self.id_str,
            "nodeName": self.nodeName,
            "sys_name": self.sys_name,
            "label": self.label,
            "isHigh": self.isHigh,
            "act_stand": self.act_stand,
            "nodeTypeStr": self.nodeTypeStr,
            "nodeType": self.get_type(),
            "size": self.get_size(),
            "type": self.type,
            "img": self.img,
            "x": self.x,
            "y": self.y,
            "canvasx": self.canvasx,
            "canvasy": self.canvasy,
            "clientx": self.clientx,
            "clienty": self.clienty,
            "manufactor": self.manufactor,
            "a_ne_index_id": self.a_ne_index_id,
            "z_ne_index_id": self.z_ne_index_id,
            "a_ne_name": self.a_ne_name,
            "z_ne_name": self.z_ne_name,
            "ocable_length": self.ocable_length
        }


class EdgeInfo(object):

    def __init__(self, source=None, target=None, isHigh=0, type=None,
                 act_stand=None, labelStr=None):
        self.source = source
        self.target = target
        self.isHigh = isHigh
        self.type = type
        self.stroke = "#10D4E7"
        self.lineWidth = 3
        self.act_stand = act_stand
        self.labelStr = labelStr
        self.label = "" if not self.labelStr or len(self.labelStr) == 0 else self.labelStr.replace('"', '')

    def to_dict(self):
        return {
            "source": self.source,
            "target": self.target,
            "isHigh": self.isHigh,
            "type": self.type,
            "act_stand": self.act_stand,
            "labelStr": self.labelStr,
            "label": self.label
        }


class SystemDetail(object):
    def __init__(self, sys_name, full_waves, fiber_lengtn, risk_sum):
        self.sys_name = sys_name
        self.full_waves = full_waves
        self.fiber_lengtn = fiber_lengtn
        self.risk_sum = risk_sum

    def to_dict(self):
        return {
            "sys_name": self.sys_name,
            "full_waves": self.full_waves,
            "fiber_lengtn": self.fiber_lengtn,
            "risk_sum": self.risk_sum
        }


def load_node(front, prefix):
    label_id = ""
    label_name = ""
    label_type = ""
    act_atand = front.act_stand
    isHigh = 0
    if prefix == "source":
        label_id = front.source_ne_id
        label_name = front.source_sub_name
        label_type = front.source_ne_type
        isHigh = front.source_ne_color
    elif prefix == "target":
        label_id = front.target_ne_id
        label_name = front.target_sub_name
        label_type = front.target_ne_type
        isHigh = front.target_ne_color

    return NodeInfo(
        id=label_id,
        sys_name=front.sys_name,
        act_stand=act_atand,
        nodeName=label_name,
        nodeTypeStr=label_type,
        type="image",
        label=label_name,
        isHigh=isHigh
    )


def find_topo_position(topo_positions, ne_id):
    for topo_pos in topo_positions:
        if topo_pos.ne_id == ne_id:
            return topo_pos
    return None


def nodelist_contains(node_list, item):
    for node in node_list:
        if node.id == item.id:
            return True
    return False


def edgelist_contains(edge_list, item):
    for edge in edge_list:
        if edge.source == item.source and edge.target == item.target and edge.act_stand == item.act_stand:
            return True
    return False


def get_nodes(fronts, topo_positions):
    nodes = []
    for front in fronts:
        item_s = load_node(front, "source")
        topo_position = find_topo_position(topo_positions, item_s.id)
        if topo_position:
            item_s.set_x(topo_position.x)
            item_s.set_y(topo_position.y)
        if not nodelist_contains(nodes, item=item_s):
            nodes.append(item_s)
            print(f"id: '{item_s.id}', x: '{item_s.x}', y: '{item_s.y}'")
        item_t = load_node(front, "target")
        topo_position = find_topo_position(topo_positions, item_t.id)
        if topo_position:
            item_t.set_x(topo_position.x)
            item_t.set_y(topo_position.y)
        if not nodelist_contains(nodes, item=item_t):
            nodes.append(item_t)
            print(f"id: '{item_t.id}', x: '{item_t.x}', y: '{item_t.y}'")
    return nodes


def find_edge(edges, source, target):
    for edge in edges:
        if (edge.source == source and edge.target == target):
            return edge
        if (edge.source == target and edge.target == source):
            return edge
    return None


def convert_edge(front, edges):
    source = front.source_ne_id
    target = front.target_ne_id
    act_stand = front.act_stand
    isHigh = front.fiber_color
    edge = find_edge(edges=edges, source=source, target=target)
    if edge:
        median = ""
        if edge.source == source:
            median = source
            source = target
            target = median

    source_type = front.source_ne_type
    target_type = front.target_ne_type
    type = "line"
    if (source_type.find('OTM') >= 0 or source_type.find('OADM') >= 0) and \
            (target_type.find('OTM') or target_type.find('OADM') >= 0):
        type = 'arc'
    edge = EdgeInfo(source=source, target=target, act_stand=act_stand,
                    labelStr=str(front.fiber_length), isHigh=isHigh, type=type)
    if not edgelist_contains(edge_list=edges, item=edge):
        edges.append(edge)


def get_edges(fronts):
    edges = []
    for front in fronts:
        convert_edge(front=front, edges=edges)
    return edges


def computed_km(m: int) -> str:
    return str(round(m // 1000)) + "km"


def set_system_label(system_name):
    s = SystemLabel.get_system_label_first(system_name=system_name, is_history=0)
    if not s:
        return None
    fiber_length = ""
    if s.sys_standby_fiber_length == 0:
        fiber_length = computed_km(s.sys_atc_fiber_length)
    else:
        fiber_length = computed_km(s.sys_atc_fiber_length) + '/' + computed_km(s.sys_standby_fiber_length)
    return SystemDetail(sys_name=s.system_name, full_waves=s.full_waves,
                        fiber_lengtn=fiber_length, risk_sum=s.risk_sum)


def topo_draw(req):
    fronts = FrontAdj.get_front_adjs(
        sys_name=req.sys_name, is_history=0)
    # load position by req
    topo_positions = TopoNePosition.get_positions(
        user_name=req.user_name,
        sys_name=req.sys_name
    )

    # C#中，结果存在 _cachePosition里, LoadNodes的实现
    nodes = get_nodes(fronts=fronts, topo_positions=topo_positions)
    edges = get_edges(fronts=fronts)
    system_label = set_system_label(system_name=req.sys_name)
    return (nodes, edges, system_label)


def order_check(site_detail, act_stands):
    if 'type' in site_detail and ("OTM" in site_detail['type'] or "OADM" in site_detail['type']) and "备" in act_stands:
        return True
    return False


def sub_name_oafingerprint_switch(site_detail, edges):
    sub_names_arr = list(site_detail['sub_nameArr'])
    calc_oms = CalcOms.get(is_history=0)
    first_oms_target_id = ""
    for i in range(len(sub_names_arr)):
        sub_names_arr[i].index = i
        oms_find = next((find for find in calc_oms if sub_names_arr[i]['ne_id'] in find.ola_all), None)
        if oms_find is None:
            continue

        sub_names_arr[i].oms_target_id = oms_find.oms_target_id if oms_find.oms_source_id == edges.self else oms_find.oms_source_id

        if i == 0:
            first_oms_target_id = sub_names_arr[i]['oms_target_id']

        if "备" not in sub_names_arr[i]['act_stand']:
            continue
        if len(sub_names_arr) <= 2:
            continue

        if sub_names_arr[i]['oms_target_id'] == first_oms_target_id:
            sub_names_arr[i]['index'] = 2
        else:
            sub_names_arr[i]['index'] = 3

    site_detail['sub_nameArr'] = sorted(sub_names_arr, key=lambda x: x.index)


def oafingerprint_switch(site_detail):
    sub_names_arr = list(site_detail['sub_nameArr'])
    calc_ne_oas = CalcNeOas.get(is_history=0)
    oafingerprint_arr = list(site_detail['mainFingerprint'])

    for i in range(len(oafingerprint_arr)):
        calc_find = next((find for find in calc_ne_oas if find.source_oa_fingerprint == oafingerprint_arr[i]['oa_fingerprintName']), None)
        if calc_find is None:
            continue
        sub_find = next((find for find in sub_names_arr if find['act_stand'] == calc_find.act_stand and find['ne_id'] == calc_find.target_ne_id), None)
        if sub_find['index'] % 2 == 0:
            if calc_find.source_oa_in_out_id == "收":
                oafingerprint_arr[i]['direction'] = "收"
                oafingerprint_arr[i]['index'] = sub_find['index'] * 2
            elif calc_find.source_oa_in_out_id == "发":
                oafingerprint_arr[i]['direction'] = "发"
                # oafingerprint_arr[i]['index'] = sub_find['index'] * 2 + 2
                oafingerprint_arr[i]['index'] = sub_find['index'] * 2 + 2
        else:
            if calc_find.source_oa_in_out_id == "收":
                oafingerprint_arr[i]['direction'] = "收"
                oafingerprint_arr[i]['index'] = (sub_find['index'] - 1) * 2 + 3
            elif calc_find.source_oa_in_out_id == "发":
                oafingerprint_arr[i]['direction'] = "发"
                oafingerprint_arr[i]['index'] = (sub_find['index'] ) * 2  - 1
                # oafingerprint_arr[i]['index'] = (sub_find['index'] - 1) * 2 + 2
    # 通过重新计算的index进行排序
    site_detail['mainFingerprint'] = sorted(oafingerprint_arr, key=lambda x: x['index'])


def get_main_site_detail(req):
    siteDetail = {}
    front_Pictures = FrontPictureOtm.get(is_history=0)
    details = FrontNe.get(is_history=0, sys_name=req.sys_name, source_ne_id=req.self)
    # details = list(filter(lambda find: find.sys_name == req.sys_name and find.source_ne_id == req.self, front_ne))
    siteFirstDetail = details[0] if len(details) > 0 else None
    type_index = siteFirstDetail.ne_type.rfind("_")
    siteDetail['sub_name'] = siteFirstDetail.source_oa_sub_name
    siteDetail['manufactor_type_model'] = siteFirstDetail.manufactor + "/" + siteFirstDetail.ne_type[type_index + 1:] + "/" + siteFirstDetail.ne_model
    sub_namesArr = []
    act_stands = []
    mainFingerprintsArr = []
    # front_find = next((find for find in front_Pictures if find.source_ne_id == req.self), None)
    front_find = next(filter(lambda find: find.source_ne_id == req.self, front_Pictures), None)
    if front_find:
        siteDetail["type"] = front_find.picture_id
    for item in details:
        sub_nameFind = next(filter(lambda find: find['subName'] == item.target_oa_sub_name and find['act_stand'] == item.act_stand, sub_namesArr), None)
        if sub_nameFind is None:
            index = len(sub_namesArr)
            sub_namesArr.append({
                "ne_id": item.target_ne_id if item.source_ne_id == req.self else item.source_ne_id,
                "subName": item.target_oa_sub_name,
                "act_stand": item.act_stand,
                "index": index
            })
            act_stands.append(item.act_stand)
        mainFingerprintsArr.append({
            "oa_fingerprintName": item.source_oa_fingerprint,
            "isHigh": item.oa_color
        })
    siteDetail["sub_nameArr"] = sub_namesArr
    siteDetail["mainFingerprint"] = mainFingerprintsArr
    if order_check(siteDetail, act_stands):
        sub_name_oafingerprint_switch(siteDetail, req)
    oafingerprint_switch(siteDetail)
    return siteDetail


def oa_fingerprintAdd(Arr, ne_id, shelf_id, slot_id, front_ne_find):
    oa_fingerprint = f"{ne_id}/{shelf_id}/{slot_id}"
    isHigh = 0
    front_find = next((find for find in front_ne_find if find.source_oa_fingerprint == oa_fingerprint), None)
    if front_find is not None:
        isHigh = front_find.oa_color
    Arr.append({
        "oa_fingerprintName": oa_fingerprint,
        "isHigh": isHigh})


def oaFingerprintCheck(type, front_Picture_OlaDetail, front_Picture_Ola, front_ne_find):
    Arr = []
    if front_Picture_Ola.oa_num > 1:
        oa_fingerprintAdd(Arr, front_Picture_Ola.source_ne_id, front_Picture_Ola.in_oa_shelf_id,
                          front_Picture_Ola.in_oa_slot_id, front_ne_find)
        oa_fingerprintAdd(Arr, front_Picture_Ola.source_ne_id, front_Picture_Ola.out_oa_shelf_id,
                          front_Picture_Ola.out_oa_slot_id, front_ne_find)
    else:
        oa_fingerprintAdd(Arr, front_Picture_Ola.source_ne_id, front_Picture_Ola.in_oa_shelf_id,
                          front_Picture_Ola.in_oa_slot_id, front_ne_find)

    if type == "source":
        front_Picture_OlaDetail['source_sub_name'] = front_Picture_Ola.in_target_ne_name
        front_Picture_OlaDetail['source_oa_fingerprintArr'] = Arr
    elif type == "target":
        front_Picture_OlaDetail['target_sub_name'] = front_Picture_Ola.in_target_ne_name
        front_Picture_OlaDetail['target_oa_fingerprintArr'] = Arr[::-1]


def get_ola_details(req):
    front_ne_find = FrontNe.get(is_history=0, sys_name=req.sys_name, source_ne_id=req.self)
    front_Picture_Olas = FrontPictureOla.get(source_ne_id=req.self, is_history=0)
    picture_Ola_first = front_Picture_Olas[0] if len(front_Picture_Olas) > 0 else None
    front_Picture_OlaDetail = {
        "id": str(picture_Ola_first.id) if picture_Ola_first else None,
        "ne_id": picture_Ola_first.source_ne_id if picture_Ola_first else None,
        "sub_name": picture_Ola_first.source_oa_sub_name if picture_Ola_first else None
    }
    for item in front_Picture_Olas:
        if 'source_sub_name' not in front_Picture_OlaDetail or len(front_Picture_OlaDetail['source_sub_name']) == 0:
            oaFingerprintCheck("source", front_Picture_OlaDetail, item, front_ne_find)
        else:
            oaFingerprintCheck("target", front_Picture_OlaDetail, item, front_ne_find)
    return front_Picture_OlaDetail


def front_data_oaDetailsAdd(front_Datas, pre_position_Voa, outing_power=0, incoming_power=0):
    return {
        "ne_incoming_power": front_Datas.ne_incoming_power,
        "outside_voa": front_Datas.outside_voa,
        "inside_voa": front_Datas.inside_voa,
        "input_power": front_Datas.input_power,
        "input_stand_power": front_Datas.input_stand_power,
        "gain": front_Datas.gain,
        "stand_gain_min": front_Datas.stand_gain_min,
        "stand_gain_max": front_Datas.stand_gain_max,
        "output_power": front_Datas.output_power,
        "output_stand_power": front_Datas.output_stand_power,
        "brd_type": front_Datas.brd_type,
        "shelf_id": front_Datas.shelf_id,
        "slot_id": front_Datas.slot_id,
        "wavs": front_Datas.wavs,
        "oms": front_Datas.oms,
        "oa_risk_num": front_Datas.oa_risk_num,
        "in_ne_subname": front_Datas.in_ne_subname,
        "out_ne_subname": front_Datas.out_ne_subname,
        "pre_position_Voa": pre_position_Voa,
        "ishigh": {
            "input_power_input_stand_power": {
                "risk_type": None,
                "is_hight": 0
                },
            "stand_gain_min_stand_gain_max": {
                "risk_type": None,
                "is_hight": 0
                },
            "output_power_output_stand_power": {
                "risk_type": None,
                "is_hight": 0
            }
        } if pre_position_Voa else {},
        "ne_outing_power": outing_power if not pre_position_Voa else 0
    }


def get_oa_details(req):
    is_history = 0
    param = req.oa_fingerpring.split('/')
    calc_Oa_Powers = CalcOaPower.get(is_history=is_history, source_ne_id=param[0], source_oa_shelf_id=param[1], source_oa_slot_id=param[2])
    pre_position_Voa = True
    outing_power = 0
    incoming_power = 0
    oa_Power_find = calc_Oa_Powers[0] if len(calc_Oa_Powers) > 0 else None
    if oa_Power_find:
        if oa_Power_find.is_voa_back == 1:
            pre_position_Voa = False
            outing_power = oa_Power_find.outing_power
            incoming_power = oa_Power_find.incoming_power
        else:
            pre_position_Voa = True
    front_Datas = FrontDataOa.get(ne_id=param[0], shelf_id=param[1], slot_id=param[2], is_history=is_history)
    if len(front_Datas) == 0:
        return None

    oaDetails = {}
    if pre_position_Voa:
        oaDetails = front_data_oaDetailsAdd(front_Datas[0], pre_position_Voa)
    else:
        oaDetails = front_data_oaDetailsAdd(front_Datas[0], pre_position_Voa, outing_power, incoming_power)
    risks = RiskOa.get(is_history=is_history, source_ne_id=param[0], source_oa_shelf_id=param[1], source_oa_slot_id=param[2])
    risk_find = risks[0] if len(risks) > 0 else None
    if risk_find:
        if risk_find.is_output_power_dev_emergency != "er_ok":
            oaDetails['ishigh']['input_power_input_stand_power']['is_hight'] = 2
            oaDetails['ishigh']['input_power_input_stand_power']['risk_type'] = risk_find.is_output_power_dev_emergency
        elif risk_find.is_output_power_dev_risk != "ok" and risk_find.is_output_power_dev_emergency == "er_ok":
            oaDetails['ishigh']['input_power_input_stand_power']['is_hight'] = 1
            oaDetails['ishigh']['input_power_input_stand_power']['risk_type'] = risk_find.is_output_power_dev_emergency

        if risk_find.is_gain_emergency != "er_ok":
            oaDetails['ishigh']["stand_gain_min_stand_gain_max"]['is_hight'] = 2
            oaDetails['ishigh']["stand_gain_min_stand_gain_max"]['risk_type'] = risk_find.is_gain_emergency
        elif risk_find.is_gain_risk != "ok" and risk_find.is_gain_emergency == "er_ok":
            oaDetails['ishigh']["stand_gain_min_stand_gain_max"]['is_hight'] = 1
            oaDetails['ishigh']["stand_gain_min_stand_gain_max"]['risk_type'] = risk_find.is_gain_emergency

        if risk_find.is_output_power_dev_emergency != "er_ok":
            oaDetails['ishigh']['output_power_output_stand_power']['is_hight'] = 2
            oaDetails['ishigh']['output_power_output_stand_power']['risk_type'] = risk_find.is_output_power_dev_emergency
        elif risk_find.is_output_power_dev_risk != "ok" and risk_find.is_output_power_dev_emergency == "er_ok":
            oaDetails['ishigh']['output_power_output_stand_power']['is_hight'] = 1
            oaDetails['ishigh']['output_power_output_stand_power']['risk_type'] = risk_find.is_output_power_dev_emergency

    oaDetails['is_history'] = is_history
    return oaDetails


def get_fiber_details(req):
    front_datas = FrontDataFiber.get_from_source_or_target(source=req.source_ne_id, target=req.target_ne_id,
                                             act_stand=req.act_stand, is_history=0)
    if front_datas is None:
        return None
    atoz_Theory_Diff = front_datas.source_out_fiber_loss - front_datas.stand_fiber_loss
    ztoa_Theory_Diff = front_datas.source_in_fiber_loss - front_datas.stand_fiber_loss
    return {
        "id": str(front_datas.id),
        "source_ne_id": front_datas.source_ne_id,
        "target_ne_id": front_datas.target_ne_id,
        "act_stand": front_datas.act_stand,
        "source_sub_name": front_datas.source_sub_name,
        "target_sub_name": front_datas.target_sub_name,
        "fiber_name": front_datas.fiber_name,
        "fiber_length": front_datas.fiber_length,
        "stand_fiber_loss": front_datas.stand_fiber_loss,
        "source_out_fiber_loss": front_datas.source_out_fiber_loss,
        "source_in_fiber_loss": front_datas.source_in_fiber_loss,
        "source_outing_power": front_datas.source_outing_power,
        "source_out_shelf_slot": front_datas.source_out_shelf_slot,
        "source_incoming_power": front_datas.source_incoming_power,
        "source_in_shelf_slot": front_datas.source_in_shelf_slot,
        "target_outing_power": front_datas.target_outing_power,
        "target_out_shelf_slot": front_datas.target_out_shelf_slot,
        "target_incoming_power": front_datas.target_incoming_power,
        "target_in_shelf_slot": front_datas.target_in_shelf_slot,
        "is_risk": front_datas.is_risk,
        "timestamp": str(front_datas.timestamp.isoformat()),
        "is_history": front_datas.is_history,
        "atoz_Theory_Diff": atoz_Theory_Diff,
        "ztoa_Theory_Diff": ztoa_Theory_Diff,
        "bothway_Diff": atoz_Theory_Diff + ztoa_Theory_Diff
    }


def set_position(req):
    topo_positions = TopoNePosition.get_positions(
        user_name=req.user_name,
        sys_name=req.sys_name,
        ne_id=req.ne_id
    )
    if len(topo_positions) == 0:
        TopoNePosition.bulk_add([req.dict()])
    else:
        TopoNePosition.update({
            "user_name": req.user_name,
            "sys_name": req.sys_name,
            "ne_id": req.ne_id},
            x=req.x, y=req.y, canvasx=req.canvasx,
            canvasy=req.canvasy, clientx=req.clientx,
            clienty=req.clienty)
