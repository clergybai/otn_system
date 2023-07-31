from ..models.front_adj import FrontAdj
from ..models.system_label import SystemLabel
from ..models.topo_ne_position import TopoNePosition


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
        self.label = "" if not self.labelStr or len(self.labelStr) else self.labelStr.replace('"', '')

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
            item_s.set_x(topo_position['x'])
            item_s.set_y(topo_position['y'])
        if not nodelist_contains(nodes, item=item_s):
            nodes.append(item_s)
        item_t = load_node(front, "target")
        topo_position = find_topo_position(topo_positions, item_t.id)
        if topo_position:
            item_t.set_x(topo_position['x'])
            item_t.set_y(topo_position['y'])
        if not nodelist_contains(nodes, item=item_t):
            nodes.append(item_t)
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
