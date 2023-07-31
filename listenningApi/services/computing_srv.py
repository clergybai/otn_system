from itertools import groupby
from ..models.computing_mode import ComputingMode
from ..models.pg_input_topology_data import PgInputTopologyData
from ..models.input_topology_data import InputTopologyData
from ..models.pg_input_oa_board_type import PgInputOaBoardType
from ..models.pg_input_voa_config import PgInputVoaConfig
from ..models.pg_input_update_timestamp import PgInputUpdateTimestamp
from ..models.input_internal_topology import InputInternalTopology
from ..models.pg_input_pm_data import PgInputPmData
from ..models.input_pm_data import InputPmData
from ..models.pg_input_optical_ne import PgInputOpticalNe
from ..models.input_optical_ne import InputOpticalNe
from ..models.pg_input_voa_back_data import PgInputVoaBackData
from ..models.input_voa_back_data import InputVoaBackData
from ..models.top_cable import TopCable
from ..models.top_gain import TopGain
from ..models.top_oa_stand import TopOaStand
from ..models.top_olp import TopOlp
from ..models.top_power_max_min import TopPowerMaxMin
from ..models.calc_fibers_sum import CalcFibersSum
from ..models.calc_incoming_optical_power import CalcIncomingOpticalPower
from ..models.calc_oa_power import CalcOaPower
from ..models.calc_ne_oas import CalcNeOas
from ..models.calc_ola_business_waves import CalcOlaBusinessWaves
from ..models.calc_otm_business_waves import CalcOtmBusinessWaves
from ..models.calc_oa_stand import CalcOaStand
from ..models.risk_fiber import RiskFiber
from ..models.risk_olp import RiskOlp
from ..models.risk_oa import RiskOa
from ..models.risk_oa_summary import RiskOaSummary
from ..models.front_picture_otm import FrontPictureOtm
from ..models.front_picture_ola import FrontPictureOla
from ..models.front_data_oa import FrontDataOa
from ..models.front_data_fiber import FrontDataFiber
from ..models.front_ne import FrontNe
from ..models.sql_raw_exec import SqlRawExec
from paramsApi.models.input_oa_board_type import InputOaBoardType
from paramsApi.models.input_oa_board_standard import InputOaBoardStandard
from paramsApi.models.input_oms_business_waves import InputOmsBusinessWaves
from paramsApi.models.input_threshold import InputThreshold
from paramsApi.models.input_std_values import InputStdValues
from paramsApi.models.calc_ne_adj import CalcNeAdj
from paramsApi.models.calc_oms import CalcOms
from webapi.models.order_list import OrderList
from webapi.models.front_adj import FrontAdj
from webapi.models.system_label import SystemLabel
from loginApi.models.front_city_permission import FrontCityPermission
from ..models.pg_input_internal_topology import PgInputInternalTopology
from paramsApi.models.input_voa_config import InputVoaConfig
from common.utils.crypto_helper import Md5Generator
from datetime import datetime, timedelta
from common.config import settings
from common.database import SqlOperation
import math
import uuid
import logging


logger = logging.getLogger(__name__)


def get_computing_state():
    return ComputingMode.get_computed_state()


def prepare():
    set_computing_mode(1)
    # 暂停线程, C#的code
    # TaskHelper.Instance.TaskSuspend();)
    
    
def CopyData():
    input_topology_datas = InputTopologyData.get(is_history=0)
    for item in input_topology_datas:
        InputTopologyData.update({"id": item['id']}, is_history=2)
    input_oa_board_types = InputOaBoardType.get_input_oa_board_types(is_history=0)
    for item in input_oa_board_types:
        InputOaBoardType.update({"id": item['id']}, is_history=2)
    input_voa_configs = InputVoaConfig.get_input_voa_configs(is_history=0)
    for item in input_voa_configs:
        InputVoaConfig.update({"id": item['id']}, is_history=2)
    input_internal_topologys = InputInternalTopology.get(is_history=0)
    for item in input_internal_topologys:
        InputInternalTopology.update({"id": item['id']}, is_history=2)
    input_pm_datas = InputPmData.get(is_history=0)
    for item in input_pm_datas:
        InputPmData.update({"id": item['id']}, is_history=2)
    input_optical_nes = InputOpticalNe.get(is_history=0)
    for item in input_pm_datas:
        InputOpticalNe.update({"id": item['id']}, is_history=2)
    input_voa_back_datas = InputVoaBackData.get(is_history=0)
    for item in input_voa_back_datas:
        InputVoaBackData.update({"id": item['id']}, is_history=2)
    

def set_computing_mode(state):
    computing_modes = ComputingMode.get_all_computing_mode()
    default_sys_name = 'DEFAULT'
    if len(computing_modes) == 0:
        ComputingMode.add(state=state, sys_name=default_sys_name)
    else:
        filters = {'sys_name': default_sys_name}
        ComputingMode.update(filters=filters, state=state)


class Computer(object):
    """_summary_
    Args:
        object (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    input_topology_datas = None
    
    def set_mysql_database(self):
        logger.info(f"{str(datetime.now())} setMysqlDatabase begin.")
        self.input_topology_datas = self.get_pg_input_topology_data()
        self.input_topology_data_add_range()
        logger.info(f"{str(datetime.now())} setMysqlDatabase Input_topology_dataAddRange end.")
        
        self.input_oa_board_type_add_range(
            self.input_oa_board_type_table_foreach(
                self.get_pg_input_oa_board_type()
            ))
        logger.info(f"{str(datetime.now())} setMysqlDatabase Input_oa_board_typeAddRange end.")
        
        self.input_voa_config_add_range(
            self.input_voa_config_table_foreach(
                self.get_pg_input_voa_config()
            )
        )
        logger.info(f"{str(datetime.now())} setMysqlDatabase Input_voa_configAddRange end.")
        self.input_internal_topology_add_range(
            self.input_internal_topology_table_foreach(
                self.get_pg_input_internal_topology()
            )
        )
        logger.info(f"{str(datetime.now())} setMysqlDatabase Input_internal_topologyAddRange end.")
        self.input_pm_data_add_range(
            self.input_pm_data_table_foreach(
                self.get_pg_input_pm_data()
            )
        )
        logger.info(f"{str(datetime.now())} setMysqlDatabase Input_pm_dataAddRange end.")
        self.input_optical_ne_add_range(
            self.get_pg_input_optical_ne()
        )
        logger.info(f"{str(datetime.now())} setMysqlDatabase Input_optical_neAddRange end.")
        self.input_voa_back_data_add_range(
            self.get_pg_input_voa_back_data()
        )
        logger.info(f"{str(datetime.now())} setMysqlDatabase end.")

    def get_pg_input_topology_data(self):
        return PgInputTopologyData.get_all()

    def get_pg_input_internal_topology(self):
        return PgInputInternalTopology.get_all()

    def get_pg_input_pm_data(self):
        return PgInputPmData.get_all()

    def get_pg_input_optical_ne(self):
        return PgInputOpticalNe.get_all()

    def get_pg_input_voa_back_data(self):
        return PgInputVoaBackData.get_all()

    def input_topology_data_add_range(self):
        kwargs_list = []
        for item in self.input_topology_datas:
            kwargs_list.append({
                "net_level": item['net_level'],
                "sys_name": item['sys_name'],
                "act_stand": item['act_stand'],
                "city": item['city'],
                "a_ne_id": item['a_ne_id'],
                "a_shelf_id": item['a_shelf_id'],
                "a_slot_id": item['a_slot_id'],
                "a_in_out_id": item['a_in_out_id'],
                "a_sub_name": item['a_sub_name'],
                "a_oa_fingerprint": item['a_oa_fingerprint'],
                "a_oa_dir_fingerprint": item['a_oa_dir_fingerprint'],
                "z_ne_id": item['z_ne_id'],
                "z_shelf_id": item['z_shelf_id'],
                "z_slot_id": item['z_slot_id'],
                "z_in_out_id": item['z_in_out_id'],
                "z_sub_name": item['z_sub_name'],
                "z_oa_fingerprint": item['z_oa_fingerprint'],
                "z_oa_dir_fingerprint": item['z_oa_dir_fingerprint'],
                "full_waves": item['full_waves'],
                "fiber_name": item['fiber_name'],
                "fiber_length": item['fiber_length'],
                "is_history": 2
            })
        InputTopologyData.bulk_add(kwargs_list)

    def input_oa_board_type_add_range(self, input_oa_board_type_list):
        kwargs_list = []
        for item in input_oa_board_type_list:
            kwargs_list.append({
                "sub_id": item['sub_id'],
                "sub_name": item['sub_name'],
                "ne_id": item['ne_id'],
                "shelf_id": item['shelf_id'],
                "slot_id": item['slot_id'],
                "board_model": item['board_model'],
                "timestamp": item['timestampstr'],
                "is_history": 2
            })
        InputOaBoardType.bulk_add(kwargs_list)

    def input_voa_config_add_range(self, input_voa_config_list):
        kwargs_list = []
        for item in input_voa_config_list:
            kwargs_list.append({
                "sub_name": item['sub_name'],
                "ne_id": item['ne_id'],
                "shelf_id": item['shelf_id'],
                "slot_id": item['slot_id'],
                "port_id": item['port_id'],
                "voa_vaule": item['voa_vaule'],
                "timestamp": item['timestamp'],
                "is_history": 2
            })
        InputVoaConfig.bulk_add(kwargs_list)

    def input_internal_topology_add_range(self, input_internal_topoloty_list):
        kwargs_list = []
        for item in input_internal_topoloty_list:
            kwargs_list.append({
                "a_sub_name": item['a_sub_name'],
                "a_ne_id": item['a_ne_id'],
                "a_shelf_id": item['a_shelf_id'],
                "a_slot_id": item['a_slot_id'],
                "a_port_id": item['a_port_id'],
                "a_in_out_id": item['a_in_out_id'],
                "a_board_model": item['a_board_model'],
                "z_sub_name": item['z_sub_name'],
                "z_ne_id": item['z_ne_id'],
                "z_shelf_id": item['z_shelf_id'],
                "z_slot_id": item['z_slot_id'],
                "z_port_id": item['z_port_id'],
                "z_in_out_id": item['z_in_out_id'],
                "z_board_model": item['z_board_model'],
                "timestamp": item['timestamp'],
                "is_history": 2
            })
        InputInternalTopology.bulk_add(kwargs_list)

    def input_pm_data_add_range(self, input_pm_data_list):
        kwargs_list = []
        for item in input_pm_data_list:
            kwargs_list.append({
                "sub_name": item['sub_name'],
                "a_ne_id": item['a_ne_id'],
                "shelf_id": item['shelf_id'],
                "slot_id": item['slot_id'],
                "port_name": item['port_name'],
                "out_power": item['out_power'],
                "in_power": item['in_power'],
                "out_power_max": item['out_power_max'],
                "out_power_min": item['out_power_min'],
                "in_power_max": item['in_power_max'],
                "in_power_min": item['in_power_min'],
                "voa_vaule": item['voa_vaule'],
                "timestamp": item['timestamp'],
                "is_history": 2
            })
        InputPmData.bulk_add(kwargs_list)

    def input_optical_ne_add_range(self, input_optical_ne_list):
        kwargs_list = []
        for item in input_optical_ne_list:
            kwargs_list.append({
                "ne_id": item['ne_id'],
                "ne_name": item['ne_name'],
                "city": item['city'],
                "district_county": item['district_county'],
                "manufactor": item['manufactor'],
                "network_level": item['network_level'],
                "ne_type": item['ne_type'],
                "ne_model": item['ne_model'],
                "timestamp": item['timestamp'],
                "is_history": 2
            })
        InputOpticalNe.bulk_add(kwargs_list)

    def input_voa_back_data_add_range(self, input_voa_back_data_list):
        kwargs_list = []
        for item in input_voa_back_data_list:
            kwargs_list.append({
                "ne_id": item['ne_id'],
                "shelf_id": item['shelf_id'],
                "slot_id": item['slot_id'],
                "vo": item['vo'],
                "timestamp": item['timestamp'],
                "is_history": 2
            })
        InputVoaBackData.bulk_add(kwargs_list)

    def get_pg_input_oa_board_type(self):
        return PgInputOaBoardType.get_all()

    def get_pg_input_voa_config(self):
        return PgInputVoaConfig.get_all()

    def ne_id_find(self, sub_name):
        data = None
        for find in self.input_topology_datas:
            if find["z_sub_name"] == sub_name or find["a_sub_name"] == sub_name:
                data = find
                break
        if data is None:
            return ""
        if sub_name == data["a_sub_name"]:
            return data["a_ne_id"]
        return data["z_ne_id"]

    def input_oa_board_type_table_foreach(self, pg_board_type_list):
        on_board_type_list = []
        for bd in pg_board_type_list:
            sub_name = bd["sub_name"]
            on_board_type_list.append({
                "sub_id": bd['sub_id'],
                "sub_name": sub_name,
                "ne_id": self.ne_id_find(sub_name),
                "shelf_id": bd['shelf_id'],
                "slot_id": bd['slot_id'],
                "board_model": bd['board_model'],
                "timestamp": bd['timestamp']
            })
        return on_board_type_list

    def input_voa_config_table_foreach(self, pg_voa_config_list):
        voa_config_list = []
        for item in pg_voa_config_list:
            sub_name = item["sub_name"]
            voa_config_list.append({
                "sub_name": sub_name,
                "ne_id": self.ne_id_find(sub_name),
                "shelf_id": item['shelf_id'],
                "slot_id": item['slot_id'],
                "port_id": item['port_id'],
                "voa_vaule": item['voa_vaule'],
                "timestamp": item['timestamp']
            })
        return voa_config_list

    def input_internal_topology_table_foreach(self, pg_internal_topology_list):
        internal_topology_list = []
        for item in pg_internal_topology_list:
            a_sub_name = item["a_sub_name"]
            z_sub_name = item["z_sub_name"]
            internal_topology_list.append({
                "a_sub_name": a_sub_name,
                "a_ne_id": self.ne_id_find(a_sub_name),
                "a_shelf_id": item['a_shelf_id'],
                "a_slot_id": item['a_slot_id'],
                "a_port_id": item['a_port_id'],
                "a_in_out_id": item['a_in_out_id'],
                "a_board_model": item['a_board_model'],
                "z_sub_name": z_sub_name,
                "z_ne_id": self.ne_id_find(z_sub_name),
                "z_shelf_id": item['z_shelf_id'],
                "z_slot_id": item['z_slot_id'],
                "z_port_id": item['z_port_id'],
                "z_in_out_id": item['z_in_out_id'],
                "z_board_model": item['z_board_model'],
                "timestamp": item['timestamp']
            })
        return internal_topology_list

    def input_pm_data_table_foreach(self, pg_input_pm_data_list):
        input_pm_data_list = []
        for item in pg_input_pm_data_list:
            sub_name = item['sub_name']
            input_pm_data_list.append({
                "sub_name": sub_name,
                "a_ne_id": self.ne_id_find(sub_name),
                "shelf_id": item['shelf_id'],
                "slot_id": item['slot_id'],
                "port_name": item['port_name'],
                "out_power": item['out_power'],
                "in_power": item['in_power'],
                "out_power_max": item['out_power_max'],
                "out_power_min": item['out_power_min'],
                "in_power_max": item['in_power_max'],
                "in_power_min": item['in_power_min'],
                "voa_vaule": item['voa_vaule'],
                "timestamp": item['timestamp']
            })
        return input_pm_data_list

    def setMy_input_update_timestamp(self):
        pg = PgInputUpdateTimestamp.get_all()
        if len(pg) == 0:
            return
        pg[0].update({
            "pg_input_topology_data": pg[0]['pg_input_topology_data'] + timedelta(seconds=1),
            "pg_input_optical_ne": pg[0]['pg_input_optical_ne'] + timedelta(seconds=1),
            "pg_input_oa_board_type": pg[0]['pg_input_oa_board_type'] + timedelta(seconds=1),
            "pg_input_voa_config": pg[0]['pg_input_voa_config'] + timedelta(seconds=1),
            "pg_input_internal_topology": pg[0]['pg_input_internal_topology'] + timedelta(seconds=1),
            "pg_input_pm_data": pg[0]['pg_input_pm_data'] + timedelta(seconds=1),
            "pg_input_voa_back_data": pg[0]['pg_input_voa_back_data'] + timedelta(seconds=1)
        })
        

computer = Computer()


def public_fuc():
    copy_arr()
    computehelper = ComputedHelper()
    is_ok = computehelper.computed()
    if is_ok:
        computer.setMy_input_update_timestamp()
    computehelper.setComputing_mode(0)


def copy_arr():
    try:
        logger.info(f"{str(datetime.now())} CopyArr begin.")
        copy_input_oa_board_standard()
        copy_input_oms_business_waves()
        copy_input_threshold()
        copy_input_std_values()
        copy_top_cable()
        copy_top_gain()
        copy_top_oa_stand()
        copy_top_olp()
        copy_top_power_max_min()
        logger.info(f"{str(datetime.now())} CopyArr end.")
    except Exception as e:
        logger.error("ERROR in CopyArr")
        logger.error(str(e))


def copy_input_oa_board_standard():
    cnt_is_history_2 = InputOaBoardStandard.get_count(is_history=2)
    if cnt_is_history_2 > 0:
        return
    input_oa_board_standards = InputOaBoardStandard.get_input_oa_board_standards(is_history=0)
    kwargs_list = []
    for item in input_oa_board_standards:
        kwargs_list.append({
            "id": item['id'],
            "is_history": 2
        })
    InputOaBoardStandard.bulk_update(kwargs_list)


def copy_input_oms_business_waves():
    if InputOmsBusinessWaves.get_count(is_history=2) > 0:
        return
    input_oms_business_waves = InputOmsBusinessWaves.get_input_oms_business_waves(is_history=0)
    kwargs_list = []
    for item in input_oms_business_waves:
        kwargs_list.append({
            "id": item['id'],
            "is_history": 2
        })
    InputOmsBusinessWaves.bulk_update(kwargs_list)


def copy_input_threshold():
    if InputThreshold.get_count(is_history=2) == 0:
        input_thresholds = InputThreshold.get_input_thresholds(is_history=0)
        kwargs_list = []
        for item in input_thresholds:
            kwargs_list.append({
                "id": item['id'],
                "is_history": 2
            })
        InputThreshold.bulk_update(kwargs_list)


def copy_input_std_values():
    if InputStdValues.get_count(is_history=2) == 0:
        input_std_values = InputStdValues.get_input_std_values(is_history=0)
        kwargs_list = []
        for item in input_std_values:
            kwargs_list.append({
                "id": item['id'],
                "is_history": 2
            })
        InputStdValues.bulk_update(kwargs_list)


def copy_top_cable():
    if TopCable.get_count(is_history=2) == 0:
        top_cables = TopCable.get_top_cables(is_history=0)
        kwargs_list = []
        for item in top_cables:
            kwargs_list.append({
                "id": item['id'],
                "is_history": 2
            })
        InputStdValues.bulk_update(kwargs_list)


def copy_top_gain():
    if TopCable.get_count(is_history=2) == 0:
        top_gains = TopCable.get_top_cables(is_history=0)
        kwargs_list = []
        for item in top_gains:
            kwargs_list.append({
                "id": item['id'],
                "is_history": 2
            })
        TopGain.bulk_update(kwargs_list)


def copy_top_oa_stand():
    if TopOaStand.get_count(is_history=2) == 0:
        top_oa_stands = TopOaStand.get_top_oa_stands(is_history=0)
        kwargs_list = []
        for item in top_oa_stands:
            kwargs_list.append({
                "id": item['id'],
                "is_history": 2
            })
        TopOaStand.bulk_update(kwargs_list)


def copy_top_olp():
    if TopOlp.get_count(is_history=2) == 0:
        top_olps = TopOlp.get_top_olps(is_history=0)
        kwargs_list = []
        for item in top_olps:
            kwargs_list.append({
                "id": item['id'],
                "is_history": 2
            })
        TopOlp.bulk_update(kwargs_list)


def copy_top_power_max_min():
    if TopPowerMaxMin.get_count(is_history=2) == 0:
        top_power_max_mins = TopPowerMaxMin.get_top_power_max_mins(is_history=0)
        kwargs_list = []
        for item in top_power_max_mins:
            kwargs_list.append({
                "id": item['id'],
                "is_history": 2
            })
        TopPowerMaxMin.bulk_update(kwargs_list)


def getCalc_ne_adjGroupFiberlength():
    cmd = "select sys_name,act_stand,sum(fiber_length) sum_fiber_length,timestamp,is_history from calc_ne_adj group by sys_name,act_stand where is_history = '0'"
    return SqlRawExec.exec(cmd)


def set_calc_ne_adj_add_range(kwargs_list):
    CalcNeAdj.bulk_add(kwargs_list)


def setCalc_fibers_sum_add_range(kwargs_list):
    CalcFibersSum.bulk_add(kwargs_list)


def setCalc_omsAddRange(DicNodeOms):
    kwargs_list = []
    _Business_Waves = InputOmsBusinessWaves.get_input_oms_business_waves(is_history = 2)
    oms_find = None
    for key, val in DicNodeOms.items():
        business_waves = val['business_waves']
        for find in _Business_Waves:
            if ((find['a_ne_id'] == val['sourceId'] and find['z_ne_id'] == val['targetId']) or \
                (find['a_ne_id'] == val['targetId'] and find['z_ne_id'] == val['sourceId'])) and \
                    find['sys_name'] == val['sys_name']:
                oms_find = find
                break
        if oms_find:
            business_waves = oms_find['business_waves']
        kwargs_list.append({
            "oms_id": key,
            "sys_name": val['sys_name'],
            "oms_source_id": val['sourceId'],
            "oms_target_id": val['targetId'],
            "act_stand": val['act_stand'],
            "business_waves": business_waves,
            "full_waves": val['full_waves'],
            "ola_all": val['oasArray'],
            "timestamp": val['timestamp'],
            "is_history": val['is_history']
        })
    CalcOms.bulk_add(kwargs_list)


def sourceOtmOrRoadmCheck(source):
    if source.find("OTM") >= 0 or source.find("OADM") >= 0:
        return True
    else:
        return False


def targetOtmOrRoadmCheck(target):
    if target.find("OTM") >= 0 or target.find("OADM") >= 0:
        return True
    else:
        return False


def getPmDataIncomingPower():
    cmd = """select ciop.oa_fingerprint,ipd.out_power,ciop.incoming_optical_power from `input_pm_data` ipd 
    inner join `calc_incoming_optical_power` ciop 
    on CONCAT(ipd.a_ne_id, '/', ipd.shelf_id, '/', ipd.slot_id) = ciop.oa_fingerprint 
    where ipd.is_history = 2 AND ciop.is_history = 2;"""
    return SqlRawExec.exec(cmd)


def getCalc_ne_oasGroup():
    cmd = """select source_ne_id,source_oa_sub_name,source_oa_shelf_id,source_oa_slot_id,source_oa_in_out_id,any_value(source_oa_fingerprint) source_oa_fingerprint, 
    source_oa_dir_fingerprint,target_ne_id,target_oa_sub_name,target_oa_shelf_id,target_oa_slot_id,target_oa_in_out_id,target_oa_fingerprint, 
    target_oa_dir_fingerprint,act_stand,full_waves,fiber_loss,timestamp,is_history 
    from db_transnet.`calc_ne_oas` group by source_oa_fingerprint;"""
    return SqlRawExec.exec(cmd)


def getComRisk_fiber():
    cmd = """select any_value(cna.source_ne_id) source_ne_id,any_value(cna.target_ne_id) target_ne_id,any_value(cna.act_stand) act_stand,group_concat(cno.fiber_loss separator ',') fiber_lossArr,coalesce(tc.manual_cable_in_out_baseline,0) manual_cable_in_out_baseline,ion.city,ion.network_level,cna.timestamp,cna.is_history 
    from db_transnet.`calc_ne_adj` cna inner join db_transnet.`calc_ne_oas` cno 
    on cna.source_ne_id = cno.source_ne_id and cna.target_ne_id = cno.target_ne_id and cna.act_stand = cno.act_stand 
    left join db_transnet.`top_cable` tc on cna.source_ne_id = tc.source_ne_id and cna.target_ne_id = tc.target_ne_id and cna.act_stand = tc.act_stand 
    inner join db_transnet.`input_optical_ne` ion on cna.source_ne_id = ion.ne_id 
    where cna.is_history = 2 and cno.is_history = 2 and ion.is_history = 2 
    group by cna.source_ne_id,cna.target_ne_id,cna.act_stand;"""
    return SqlRawExec.exec(cmd)


def getInput_internal_topologyOLP():
    cmd = """select * from db_transnet.`input_internal_topology` where 
    ((a_board_model like '%OLP%' and (z_board_model like '%OAU%' or z_board_model like '%OBU%') and z_in_out_id = '发') or 
    (z_board_model like '%OLP%' and (a_board_model like '%OAU%' or a_board_model like '%OBU%') and a_in_out_id = '发')) 
    and is_history = 2;"""
    return SqlRawExec.exec(cmd)


def getFront_picture_otmCom():
    cmd = f"""select any_value(cobw.source_ne_id) source_ne_id,ion.ne_type,cobw.timestamp from {Constants.MysqlDbName }`calc_otm_business_waves` cobw 
    inner join {settings.db_tr_schema}.`input_optical_ne` ion 
    on cobw.source_ne_id = ion.ne_id 
    where cobw.is_history = 2 group by cobw.source_ne_id;"""
    return SqlRawExec.exec(cmd)


def getFront_picture_olaCom():
    cmd = f"""select cno.source_ne_id,cno.source_oa_sub_name,cno.source_oa_shelf_id,cno.source_oa_slot_id,cno.target_ne_id,cno.target_oa_sub_name,ion.ne_type,cno.timestamp from {Constants.MysqlDbName }`calc_ne_oas` cno 
    inner join {settings.db_tr_schema}.`input_optical_ne` ion 
    on cno.source_ne_id = ion.ne_id where cno.source_oa_in_out_id = '收' and ion.ne_type like '%OLA%' and cno.is_history = 2;"""
    return SqlRawExec.exec(cmd)

def getSystem_label_Com():
    cmd = f"""select co.sys_name,co.full_waves,cfs.sum_fibers_length,any_value(cfs.sys_name) sys_name,any_value(cfs.act_stand) act_stand,co.timestamp 
    from {settings.db_tr_schema}.`calc_oms` co right join {settings.db_tr_schema}.`calc_fibers_sum` cfs 
    on co.sys_name = cfs.sys_name where co.is_history = 2 group by cfs.sys_name,cfs.act_stand;"""
    return SqlRawExec.exec(cmd)


def MysqltableOperation(operation, oldVal=0, newVal=0):
    tableName = ["calc_fibers_sum", "calc_incoming_optical_power", "calc_ne_adj",
                 "calc_ne_oas", "calc_oa_power", "calc_oa_stand", "calc_ola_business_waves", 
                 "calc_oms", "calc_otm_business_waves", "calc_outing_optical_power",
                 "calc_outputing_optical_power", "front_color_oa", "front_data_fiber",
                 "front_data_oa" , "front_ne", "front_adj", "front_picture_ola",
                 "front_picture_otm", "input_internal_topology", "input_oa_board_standard",
                 "input_oa_board_type", "input_oms_business_waves", "input_optical_ne",
                 "input_pm_data", "input_std_values", "input_threshold", "input_topology_data",
                 "input_voa_back_data", "input_voa_config", "order_list", "output_oms_business_waves",
                 "risk_fiber", "risk_oa", "risk_oa_summary", "risk_olp","system_label", "top_cable",
                 "top_gain", "top_oa_stand", "top_olp", "top_power_max_min"]
    cmds = []
    for item in tableName:
        if operation == SqlOperation.UPDATE.value:
            cmds.append(f"update {settings.db_tr_schema}.`{item}` set is_history = {newVal} where is_history = {oldVal};")
        elif operation == SqlOperation.DELETE.value:
            cmds.append(f"delete from {settings.db_tr_schema}.`{item}` where is_history = {oldVal};")
    
    for cmd in cmds:
        SqlRawExec.exec(cmd)
    
    sql = f"update db_login.`front_city_permission` set is_history = {newVal} where is_history = {oldVal};"
    SqlRawExec.exec(sql)


def deleteDataState(tabName, is_historyArr):
    if len(is_historyArr) == 0:
        return
    is_historys = f"({','.join(is_historyArr)})"
    cmd = f"DELETE FROM {settings.db_tr_schema}.`{tabName}` WHERE is_history in {is_historys};"
    SqlRawExec.exec(cmd)


def removeDataState(tabName, oldIs_history, newIs_history):
    cmd = f"UPDATE {settings.db_tr_schema}.`{tabName}` SET is_history = {newIs_history} WHERE is_history = {oldIs_history};"
    SqlRawExec.exec(cmd)


def getInput_thresholdCopy():
    input_thresholds = InputThreshold.get_input_thresholds(is_history=2)
    if len(input_thresholds) == 0:
        return InputThreshold.get_input_thresholds(is_history=0)
    return None


def ne_typeFind(input_Optical_Nes, ne_id):
    ne_type = ""
    Ne_find = None
    for find in input_Optical_Nes:
        if find['ne_id'] == ne_id:
            Ne_find = find
            break
    if Ne_find:
        ne_type = Ne_find['ne_type']
    return ne_type


def omsFind(_Oms, check, target_ne_id, source_ne_id):
    if check:
        for item in _Oms:
            if (item['oms_source_id'] == source_ne_id and item['oms_target_id'] == target_ne_id) or \
                (item['oms_source_id'] == target_ne_id and item['oms_target_id'] == source_ne_id):
                return item
    else:
        for item in _Oms:
            if  item['ola_all'].find(target_ne_id) >= 0:
                return item
    return None


def _optical_neFind(input_Optical_Nes, oms_ne_id):
    for find in input_Optical_Nes:
        if find['ne_id'] == oms_ne_id:
            return find
    return None


def Input_thresholdFind(data, city, net_level):
    findThreshold = None
    if data is None:
        return findThreshold
    if net_level.find("二干") >= 0:
        for item in data:
            if item['net_level'].find("二干") and item['is_used'] == 1:
                findThreshold = item
                break
    else:
        for item in data:
            if item['city'] == city and item['is_used'] == 1:
                findThreshold = item
                break
    if findThreshold is None:
        for item in data:
            if item['rule_name'] == "default":
                findThreshold = item
                break
    return findThreshold
        

def computed_input_Pm_Data_find(input_Pm_Data_find, power, input_Threshold,
                                top_gain, top_oa, calc_Oa_Stand_find, optical_power_baseline,
                                gain_baseline, obj_risk_oa):
    sum_risks = 0
    is_input_power_fluc_risk = ""
    is_input_power_fluc_emergency = ""
    is_output_power_fluc_risk = ""
    is_output_power_fluc_emergency = ""
    is_gain_risk = ""
    is_gain_emergency = ""
    is_output_power_dev_risk = ""
    is_output_power_dev_emergency = ""
    
    out_power = input_Pm_Data_find['out_power']
    out_power_min = input_Pm_Data_find['out_power_min']
    out_power_max = input_Pm_Data_find['out_power_max']
    in_power = input_Pm_Data_find['in_power']
    in_power_min = input_Pm_Data_find['in_power_min']
    in_power_max = input_Pm_Data_find['in_power_max']
    
    oa_input_power_fluc_risk = 0
    oa_output_power_fluc_risk = 0
    oa_gain_std_dev_risk = 0
    oa_output_power_std_dev_risk = 0
    standard_wave_output = 0
    
    if calc_Oa_Stand_find and top_oa is None:
        standard_wave_output = calc_Oa_Stand_find['standard_wave_output']
    elif top_oa:
        standard_wave_output = top_oa['manual_standard_wave_output']


class ComputedHelper():
    NodeOms = []
    DicNodeOMS = dict()
    OasSQL = ""
    separator = "=>"
    slash = "/"
    send = "发"
    siteOTM = "OTM"
    siteROADM = "OADM"
    put = "收"
    ok = "ok"
    er_ok = "er_ok"

    def get_topologys_data_input_optical_ne(self):
        cmd = """SELECT itd.*,ion_a.ne_type a_ne_type,ion_z.ne_type z_ne_type  from `input_topology_data` itd 
        inner join `input_optical_ne` ion_a on itd.a_ne_id = ion_a.ne_id inner join `input_optical_ne` ion_z 
        on itd.z_ne_id = ion_z.ne_id;"""
        return SqlRawExec.exec(cmd)
    
    def Computed_ne_color(self, front_ne_Data, risk_oa_Data, sys_name, ne_id):
        front_ne_find = list(filter(lambda find: find['source_ne_id'] == ne_id and find['sys_name'] == sys_name, front_ne_Data))
        if front_ne_find and len(front_ne_find) > 0:
            find_Count = 0
            risk_oa_find = []
            for item in front_ne_find:
                oa = next(
                    filter(lambda find: find['source_ne_id'] == item['source_ne_id'] and find['source_oa_shelf_id'] == item['source_oa_shelf_id'] and \
                        find['source_oa_slot_id'] == item['source_oa_slot_id'], risk_oa_Data), None)
                if oa:
                    risk_oa_find.append(oa)
            find_Count = len(risk_oa_find)
            source_ne_color_find = list(filter(lambda find: find['is_input_power_fluc_emergency'] == self.er_ok and find['is_output_power_fluc_emergency'] == self.er_ok and find['is_output_power_dev_emergency'] == self.er_ok, risk_oa_find))
            if len(source_ne_color_find) == find_Count:
                source_ne_color_find = list(filter(lambda find: find['is_input_power_fluc_risk'] == self.ok and find['is_output_power_fluc_risk'] == self.ok and find['is_gain_risk'] == self.ok and find['is_output_power_dev_risk'] == self.ok, risk_oa_find))
                if len(source_ne_color_find) == find_Count:
                    return 0
                else:
                    return 1
            else:
                return 2
        
        return 0
    
    def Computed_fiber_color(self, risk_fiber_Data, source_ne_id, target_ne_id, acr_stand):
        risk_fiber_find = next(
            filter(lambda find: ((find['source_ne_id'] == source_ne_id and find['target_ne_id'] == target_ne_id) or (find['source_ne_id'] == target_ne_id and \
                find['target_ne_id'] == source_ne_id)) and find['act_stand'] == acr_stand, risk_fiber_Data), None)
        if risk_fiber_find:
            if risk_fiber_find['is_emergency'] == self.er_ok:
                if risk_fiber_find['is_risk'] == self.ok:
                    return 0
                else:
                    return 1
            else:
                return 2
        return 0

    def computed_calc_ne_adj(self):
        data = self.get_topologys_data_input_optical_ne()
        calc_ne_adj = []
        for item in data:
            if item['a_in_out_id'] == "发":
                calc_ne_adj.append({
                    "source_ne_id": item['a_ne_id'],
                    "target_ne_id": item['z_ne_id'],
                    "source_sub_name": item['a_sub_name'],
                    "target_sub_name": item['z_sub_name'],
                    "act_stand": item['act_stand'],
                    "full_waves": item['full_waves'],
                    "sys_name": item['sys_name'],
                    "fiber_name": item['fiber_name'],
                    "fiber_length": item['fiber_length'],
                    "net_level": item['net_level'],
                    "source_ne_type": item['a_ne_type'],
                    "target_ne_type": item['z_ne_type'],
                    "timestamp": item['timestamp'],
                    "is_history": 2
                })
        calc_Ne_Adjs = []
        for item in calc_ne_adj:
            find = None
            for it in calc_Ne_Adjs:
                if (it["source_ne_id"] == item["source_ne_id"] and it["target_ne_id"] == item["target_ne_id"]) or \
                    (it["source_ne_id"] == item["target_ne_id"] and it["target_ne_id"] == item["source_ne_id"]) and it["act_stand"] == item["act_stand"]:
                    find = item
                    break
            if find:
                calc_Ne_Adjs.append(item)
        set_calc_ne_adj_add_range(calc_Ne_Adjs)

    def AddDicNodeOMS(self, item):
        sql = "" if len(self.OasSQL) == 0 else self.OasSQL.rstrip(self.separator).replace(' ', '')
        sqllArray = sql.split(self.separator)
        oms = {
            "sourceId": item['sourceId'],
            "sourceType": item['sourceType'],
            "targetId": item['targetId'],
            "targetType": item['targetType'],
            "act_stand": item['act_stand'],
            "sys_name": item['sys_name'],
            "business_waves": item['business_waves'],
            "full_waves": item['full_waves'],
            "oasArray": sql,
            "timestamp": item['timestamp'],
            "is_history": item['is_history']
        }
        oms['sourceId'] = sqllArray[0]
        oms['targetId'] = sqllArray[len(sqllArray) -1]
        source_id = oms['sourceId']
        target_id = oms['targetId']
        act_stand = "-" + oms.act_stand if item['act_stand'] is None or item['act_stand'] == "" else ""
        key = source_id + "-" + target_id + act_stand
        keyReverse = target_id + "-" + source_id + act_stand
        if key not in self.DicNodeOMS and keyReverse not in self.DicNodeOMS:
            self.DicNodeOMS[key] = oms

    def computed_is_power_fluc_risk(self, power_max, power_min, optical_power_baseline,
                                    oa_power_fluc_risk_thr, oa_power_fluc_risk_urg,
                                    is_power_fluc_risk, is_power_fluc_emergency, sum_risks,
                                    oa_power_fluc_risk):
        oa_power_fluc_risk = abs(power_max - power_min)
        oa_power_fluc_risk -= optical_power_baseline
        if oa_power_fluc_risk <= oa_power_fluc_risk_thr:
            is_power_fluc_risk = self.ok
            is_power_fluc_emergency = self.er_ok
            return (is_power_fluc_risk, is_power_fluc_emergency, sum_risks, oa_power_fluc_risk)
        
        sum_risks += 1
        is_power_fluc_risk = "high"
        if oa_power_fluc_risk > oa_power_fluc_risk_urg:
            is_power_fluc_emergency = "higher"
        else:
            is_power_fluc_emergency = self.er_ok
        return (is_power_fluc_risk, is_power_fluc_emergency, sum_risks, oa_power_fluc_risk)

    def computed_is_gain_risk_sub(self, oa_gain_std_dev_risk, gain_baseline, oa_gain_std_dev_risk_thr, oa_gain_std_dev_risk_urg,
                                  is_gain_risk, is_gain_emergency, sum_risks):
        is_lower = False
        if oa_gain_std_dev_risk < 0:
            oa_gain_std_dev_risk = abs(oa_gain_std_dev_risk)
            is_lower = True
        
        oa_gain_std_dev_risk -= gain_baseline
        if oa_gain_std_dev_risk <= oa_gain_std_dev_risk_thr:
            is_gain_risk = self.ok
            is_gain_emergency = self.er_ok
            return (is_gain_risk, is_gain_emergency, sum_risks)
        sum_risks += 1
        is_gain_risk = "low" if is_lower else "high"
        if oa_gain_std_dev_risk > oa_gain_std_dev_risk_urg:
            is_gain_emergency = "lower" if is_lower else "higher"
        else:
            is_gain_emergency = self.er_ok
        return (is_gain_risk, is_gain_emergency, sum_risks)

    def computed_is_gain_risk(self, out_power, in_power, standard_gain_min, standard_gain_max,
                              gain_baseline, input_Threshold,
                              is_gain_risk, is_gain_emergency, sum_risks, oa_gain_std_dev_risk):
        oa_gain_std_dev_risk = 0
        if standard_gain_min > standard_gain_max:
            is_gain_risk = self.ok
            is_gain_emergency = self.er_ok
            return (is_gain_risk, is_gain_emergency, sum_risks, oa_gain_std_dev_risk)
        delta_power = out_power - in_power
        if delta_power <= standard_gain_max and delta_power >= standard_gain_min:
            is_gain_risk = self.ok
            is_gain_emergency = self.er_ok
            return (is_gain_risk, is_gain_emergency, sum_risks, oa_gain_std_dev_risk)
        if delta_power > standard_gain_max:
            oa_gain_std_dev_risk = delta_power - standard_gain_max
            result = self.computed_is_gain_risk_sub(
                oa_gain_std_dev_risk, gain_baseline, input_Threshold['oa_gain_std_dev_up_risk_thr'], input_Threshold['oa_gain_std_dev_up_risk_urg'],
                is_gain_risk, is_gain_emergency, sum_risks)
            is_gain_risk, is_gain_emergency, sum_risks = result
        elif delta_power < standard_gain_min:
            oa_gain_std_dev_risk = delta_power - standard_gain_min
            result = self.computed_is_gain_risk_sub(
                oa_gain_std_dev_risk, gain_baseline, input_Threshold['oa_gain_std_dev_low_risk_thr'], input_Threshold['oa_gain_std_dev_low_risk_urg'],
                is_gain_risk, is_gain_emergency, sum_risks)
            is_gain_risk, is_gain_emergency, sum_risks = result
        return (is_gain_risk, is_gain_emergency, sum_risks, oa_gain_std_dev_risk)

    def computed_is_output_power_dev_risk_sub(
        self, oa_output_power_std_dev_risk_Check, risk_thr, risk_urg,
        is_output_power_dev_risk, is_output_power_dev_emergency, sum_risks):
        is_lower = False
        if oa_output_power_std_dev_risk_Check < 0:
            oa_output_power_std_dev_risk_Check = abs(oa_output_power_std_dev_risk_Check)
            is_lower = True
        
        if oa_output_power_std_dev_risk_Check <= risk_thr:
            is_output_power_dev_risk = self.ok
            is_output_power_dev_emergency = self.er_ok
            return (is_output_power_dev_risk, is_output_power_dev_emergency, sum_risks)
        sum_risks += 1
        is_output_power_dev_risk = "low" if is_lower else "high"
        if oa_output_power_std_dev_risk_Check > risk_urg:
            is_output_power_dev_emergency = "lower" if is_lower else "higher"
        else:
            is_output_power_dev_emergency = self.er_ok

    def computed_is_output_power_dev_risk(
        self, out_power, standard_wave_output, input_Threshold,
        is_output_power_dev_risk, is_output_power_dev_emergency, sum_risks, oa_output_power_std_dev_risk):
        oa_output_power_std_dev_risk_Check = out_power - standard_wave_output
        oa_output_power_std_dev_risk = out_power
        if oa_output_power_std_dev_risk_Check == 0:
            is_output_power_dev_risk = self.ok
            is_output_power_dev_emergency = self.er_ok
            return (is_output_power_dev_risk, is_output_power_dev_emergency, sum_risks, oa_output_power_std_dev_risk)
        if oa_output_power_std_dev_risk_Check > 0:
            result = self.computed_is_output_power_dev_risk_sub(
                oa_output_power_std_dev_risk_Check, input_Threshold['oa_output_power_std_dev_up_risk_thr'], input_Threshold['oa_output_power_std_dev_up_risk_urg'],
                is_output_power_dev_risk, is_output_power_dev_emergency, sum_risks)
            is_output_power_dev_risk, is_output_power_dev_emergency, sum_risks = result
        elif oa_output_power_std_dev_risk_Check < 0:
            result = self.computed_is_output_power_dev_risk_sub(
                oa_output_power_std_dev_risk_Check, input_Threshold['oa_output_power_std_dev_low_risk_thr'], input_Threshold['oa_output_power_std_dev_low_risk_urg'],
                is_output_power_dev_risk, is_output_power_dev_emergency, sum_risks)
            is_output_power_dev_risk, is_output_power_dev_emergency, sum_risks = result
        return (is_output_power_dev_risk, is_output_power_dev_emergency, sum_risks, oa_output_power_std_dev_risk)

    def computed_input_Pm_Data_find(self, input_Pm_Data_find, power, input_Threshold,
                                    top_gain, top_oa, calc_Oa_Stand_find, optical_power_baseline,
                                    gain_baseline, obj_risk_oa):
        sum_risks = 0
        is_input_power_fluc_risk = ""
        is_input_power_fluc_emergency = ""
        is_output_power_fluc_risk = ""
        is_output_power_fluc_emergency = ""
        is_gain_risk = ""
        is_gain_emergency = ""
        is_output_power_dev_risk = ""
        is_output_power_dev_emergency = ""
        
        out_power = input_Pm_Data_find['out_power']
        out_power_min = input_Pm_Data_find['out_power_min']
        out_power_max = input_Pm_Data_find['out_power_max']
        in_power = input_Pm_Data_find['in_power']
        in_power_min = input_Pm_Data_find['in_power_min']
        in_power_max = input_Pm_Data_find['in_power_max']
        
        oa_input_power_fluc_risk = 0
        oa_output_power_fluc_risk = 0
        oa_gain_std_dev_risk = 0
        oa_output_power_std_dev_risk = 0
        standard_wave_output = 0
        
        if calc_Oa_Stand_find and top_oa is None:
            standard_wave_output = calc_Oa_Stand_find['standard_wave_output']
        elif top_oa:
            standard_wave_output = top_oa['manual_standard_wave_output']
        result = self.computed_is_power_fluc_risk(
            in_power_max, in_power_min, optical_power_baseline, input_Threshold['oa_input_power_fluc_risk_thr'],
            input_Threshold['oa_input_power_fluc_risk_urg'], is_input_power_fluc_risk,
            is_input_power_fluc_emergency, sum_risks, oa_input_power_fluc_risk)
        is_input_power_fluc_risk, is_input_power_fluc_emergency, sum_risks, oa_input_power_fluc_risk = result
        result = self.computed_is_power_fluc_risk(
            out_power_max, out_power_min, optical_power_baseline,
            input_Threshold['oa_output_power_fluc_risk_thr'], input_Threshold['oa_output_power_fluc_risk_urg'],
            is_output_power_fluc_risk, is_output_power_fluc_emergency, sum_risks, oa_output_power_fluc_risk)
        is_output_power_fluc_risk, is_output_power_fluc_emergency, sum_risks, oa_output_power_fluc_risk = result
        if calc_Oa_Stand_find:
            if calc_Oa_Stand_find['standard_gain_min'] != 0 and calc_Oa_Stand_find['standard_gain_max'] != 0:
                result = self.computed_is_gain_risk(
                    out_power, in_power, calc_Oa_Stand_find['standard_gain_min'], calc_Oa_Stand_find['standard_gain_max'], gain_baseline, input_Threshold,
                    is_gain_risk, is_gain_emergency, sum_risks, oa_gain_std_dev_risk)
                is_gain_risk, is_gain_emergency, sum_risks, oa_gain_std_dev_risk = result
            else:
                is_gain_risk = self.ok
                is_gain_emergency = self.er_ok
        else:
            is_gain_risk = self.ok
            is_gain_emergency = self.er_ok
        result = self.computed_is_output_power_dev_risk(
            out_power, standard_wave_output, input_Threshold,
            is_output_power_dev_risk, is_output_power_dev_emergency, sum_risks, oa_output_power_std_dev_risk)
        is_output_power_dev_risk, is_output_power_dev_emergency, sum_risks, oa_output_power_std_dev_risk = result
        
        obj_risk_oa['oa_input_power_fluc_risk'] = oa_input_power_fluc_risk
        obj_risk_oa['optical_power_baseline'] = optical_power_baseline
        obj_risk_oa['is_input_power_fluc_risk'] = is_input_power_fluc_risk
        obj_risk_oa['is_input_power_fluc_emergency'] = is_input_power_fluc_emergency
        obj_risk_oa['oa_output_power_fluc_risk'] = oa_output_power_fluc_risk
        obj_risk_oa['is_output_power_fluc_risk'] = is_output_power_fluc_risk
        obj_risk_oa['is_output_power_fluc_emergency'] = is_output_power_fluc_emergency
        obj_risk_oa['oa_gain_std_dev_risk'] = oa_gain_std_dev_risk
        obj_risk_oa['gain_baseline'] = gain_baseline
        obj_risk_oa['is_gain_risk'] = is_gain_risk
        obj_risk_oa['is_gain_emergency'] = is_gain_emergency
        obj_risk_oa['oa_output_power_std_dev_risk'] = oa_output_power_std_dev_risk
        obj_risk_oa['standard_wave_output'] = standard_wave_output
        obj_risk_oa['is_output_power_dev_risk'] = is_output_power_dev_risk
        obj_risk_oa['is_output_power_dev_emergency'] = is_output_power_dev_emergency
        obj_risk_oa['sum_risks'] = sum_risks
        return obj_risk_oa

    def computed_input_Pm_Data_not_find(self, power, input_Threshold, top_gain, top_oa, calc_Oa_Stand_find,
                                        optical_power_baseline, gain_baseline,
                                        obj_risk_oa):
        sum_risks = 0
        oa_input_power_fluc_risk = 0
        oa_output_power_fluc_risk = 0
        oa_gain_std_dev_risk = 0
        oa_output_power_std_dev_risk = 0
        standard_wave_output = 0
        in_power = 0
        in_power_max = 0
        in_power_min = 0
        out_power = 0
        out_power_max = 0
        out_power_min = 0
        standard_gain_min = 0
        standard_gain_max = 0

        if calc_Oa_Stand_find and top_oa is None:
            standard_wave_output = calc_Oa_Stand_find['standard_wave_output']
        elif top_oa:
            standard_wave_output = top_oa['manual_standard_wave_output']
        oa_input_power_fluc_risk = abs(in_power_max - in_power_min)
        oa_output_power_fluc_risk = abs(out_power_max - out_power_min)
        if (out_power - in_power) > standard_gain_max:
            oa_gain_std_dev_risk = out_power - in_power - standard_gain_max
        elif (out_power - in_power) < standard_gain_min:
            oa_gain_std_dev_risk = out_power - in_power - standard_gain_min
        else:
            oa_gain_std_dev_risk = 0
        
        oa_output_power_std_dev_risk = out_power

        obj_risk_oa['oa_input_power_fluc_risk'] = oa_input_power_fluc_risk
        obj_risk_oa['optical_power_baseline'] = optical_power_baseline
        obj_risk_oa['is_input_power_fluc_risk'] = self.ok
        obj_risk_oa['is_input_power_fluc_emergency'] = self.er_ok
        obj_risk_oa['oa_output_power_fluc_risk'] = oa_output_power_fluc_risk
        obj_risk_oa['is_output_power_fluc_risk'] = self.ok
        obj_risk_oa['is_output_power_fluc_emergency'] = self.er_ok
        obj_risk_oa['oa_gain_std_dev_risk'] = oa_gain_std_dev_risk
        obj_risk_oa['gain_baseline'] = gain_baseline
        obj_risk_oa['is_gain_risk'] = self.ok
        obj_risk_oa['is_gain_emergency'] = self.er_ok
        obj_risk_oa['oa_output_power_std_dev_risk'] = oa_output_power_std_dev_risk
        obj_risk_oa['standard_wave_output'] = standard_wave_output
        obj_risk_oa['is_output_power_dev_risk'] = self.ok
        obj_risk_oa['is_output_power_dev_emergency'] = self.er_ok
        obj_risk_oa['sum_risks'] = sum_risks
        return obj_risk_oa

    def computed_calc_part1(self):
        self.computed_calc_ne_adj()
        self.computed_calc_fibers_sum()
        self.ComputedClac_oms()
        self.ComputedCalc_incoming_optical_power()
        self.ComputedCalc_oa_power()
        self.ComputedCalc_ne_oas()
        
    def computed_calc_part2(self):
        # ComputedCalc_ola_Business_waves
        self.ComputedCalc_ola_Business_waves()
        self.ComputedCalc_otm_bussiness_waves()
        self.ComputedCalc_oa_stand()
        
    def computed_risk(self):
        self.ComputedRisk_fiber()
        self.ComputedRisk_olp()
        self.ComputedRisk_oa()
        self.ComputedRisk_oa_summary()
        
    def ComputedOther(self):
        self.ComputedOrder_list()
        self.ComputedFront_picture_otm()
        self.ComputedFront_picture_ola()
        self.ComputedFront_data_oa()
        self.ComputedFront_data_fiber()
        self.ComputedFront_city_Permission()
        self.ComputedFront_ne()
        self.ComputedFront_adj()
        self.ComputedSystem_label()
        
    def sqlTableOperation(self):
        self.RemoveIshistoryOne()
        self.UpdateIshistoryZero_One()
        self.UpdateIshistoryTwo_Zero()

    def computed(self) -> bool:
        result = False
        try:
            logger.info(f"{str(datetime.now())} ComputedCalcPart1 begin.")
            self.computed_calc_part1()
            result = True
        except Exception as ex:
            logger.error(f"ERROR in ComputedCalcPart1: {str(ex)}")
            result = False
        logger.info(f"{str(datetime.now())}  ComputedCalcPart1 end. {str(result)}")
        
        try:
            if result:
                logger.info(f"{str(datetime.now())} ComputedCalcPart2 begin.")
                self.computed_calc_part2()
        except Exception as ex:
            logger.error(f"ERROR in ComputedCalcPart2: {str(ex)}")
            result = False
        logger.info(f"{str(datetime.now())}  ComputedCalcPart2 end. {str(result)}")
        
        try:
            if result:
                logger.info(f"{str(datetime.now())} ComputedRisk begin.")
                self.computed_risk()
        except Exception as ex:
            logger.error(f"ERROR in ComputedRisk: {str(ex)}")
            result = False
        logger.info(f"{str(datetime.now())} ComputedRisk end. {str(result)}")
        
        try:
            if result:
                logger.info(f"{str(datetime.now())} ComputedOther begin.")
                self.ComputedOther()
        except Exception as ex: 
            logger.error(f"ERROR in ComputedOther: {str(ex)}")
            result = False
        logger.info(f"{str(datetime.now())} ComputedOther end. {str(result)}")
        
        try:
            if result:
                logger.info("calc ok.")
                self.sqlTableOperation()
                self.sendSingle()
            else:
                logger.info("calc not ok.")
                MysqltableOperation(SqlOperation.UPDATE.value, 12, 13)
                MysqltableOperation(SqlOperation.UPDATE.value, 2, 12)
                self.rollback()
        except Exception as ex:
            logger.error(f"ERROR in sqlTableOperation: {str(ex)}")
            result = False
        return result

    def computed_calc_fibers_sum(self):
        data = getCalc_ne_adjGroupFiberlength()
        fibers_Sums = []
        for item in data:
            fibers_Sums.append({
                "sys_name": item["sys_name"],
                "act_stand": item['act_stand'],
                "sum_fibers_length": item['sum_fibers_length'],
                "timestamp": item['timestamp'],
                "is_history": 2
            })
        setCalc_fibers_sum_add_range(fibers_Sums)

    def getOasArray(self, equal, unequal, act_stand, direction):
        if direction:
            self.OasSQL = self.OasSQL + unequal + self.separator
        else:
            self.OasSQL = unequal + self.separator + self.OasSQL
            
        res = None
        for item in self.NodeOms:
            if (item['sourceId'] == equal or item['targetId'] == equal) and \
                (item['sourceId'] != unequal and item['targetId'] != unequal) and \
                    item['act_stand'] == act_stand:
                res = item
        if res is None:
            return
        if sourceOtmOrRoadmCheck(res["sourceType"]) or targetOtmOrRoadmCheck(res['targetType']):
            if sourceOtmOrRoadmCheck(res["sourceType"]):
                if direction:
                    self.OasSQL = self.OasSQL + res['targetId'] + self.separator + res['sourceId'] + self.separator
                else:
                    self.OasSQL = res['sourceId'] + self.separator + res['targetId'] + self.separator + self.OasSQL
            elif targetOtmOrRoadmCheck(res['targetType']):
                if direction:
                    self.OasSQL = self.OasSQL + res['sourceId'] + self.separator + res['targetId'] + self.separator
                else:
                    self.OasSQL = res['targetId'] + self.separator + res['sourceId'] + self.separator + self.OasSQL
                return
        else:
            if equal == res['sourceId']:
                self.getOasArray(res['targetId'], res['sourceId'], act_stand, direction)
            else:
                self.getOasArray(res['sourceId'], res['targetId'], act_stand, direction)

    def ComputedClac_oms(self):
        data = CalcNeAdj.get(is_history=0)
        for item in data:
            self.NodeOms.append({
                "sourceId": item['sourceId'],
                "sourceType": item['sourceType'],
                "targetId": item['targetId'],
                "targetType": item['targetType'],
                "act_stand": item['act_stand'],
                "sys_name": item['sys_name'],
                "business_waves": 30,
                "full_waves": item['full_waves'],
                "timestamp": item['timestamp'],
                "is_history": item['is_history']
            })
        nodeOTM = list(filter(
            lambda x: sourceOtmOrRoadmCheck(x['sourceType'] or targetOtmOrRoadmCheck(x['targetType'])), self.NodeOms))
        for item in nodeOTM:
            if sourceOtmOrRoadmCheck(item["sourceType"]) and targetOtmOrRoadmCheck(item["targetType"]):
                source_id = item['sourceId']
                target_id = item['targetId']
                act_stand = "" if item['act_stand'] is None or len(item["act_stand"]) == 0 else "-" + item['act_stand']
                key = source_id + "-" + target_id + act_stand
                keyReverse = target_id + "-" + source_id + act_stand
                if key not in self.DicNodeOMS and keyReverse not in self.DicNodeOMS:
                    self.DicNodeOMS[key] = item
            elif sourceOtmOrRoadmCheck(item["sourceType"]):
                self.getOasArray(item['sourceId'], item['targetId'], item['act_stand'], False)
                self.AddDicNodeOMS(item)
            else:
                self.getOasArray(item['sourceId'], item['targetId'], item['act_stand'], False)
                self.AddDicNodeOMS(item)
        setCalc_omsAddRange(self.DicNodeOMS)
            
    def ComputedCalc_incoming_optical_power(self):
        calc_Incoming_Opticals = InputTopologyData.get(is_history=2)
        input_Pm_Datas = InputPmData.get(is_history=2)
        input_Voa_Configs = InputVoaConfig.get_input_voa_configs(is_history=2)
        input_Internal_Topologies = InputInternalTopology.get(is_history=2)
        _Incoming_Optical = []
        calc_Incomings = []
        for item in calc_Incoming_Opticals:
            a_power = 0
            z_power = 0
            input_Pm_find_a = None
            for find in input_Pm_Datas:
                if (find['a_ne_id'] + self.slash + find['shelf_id'] + self.slash + find['slot_id']) == item['a_oa_fingerprint']:
                    input_Pm_find_a = find
                    break
            input_Pm_find_z = None
            for find in input_Pm_Datas:
                if (find['a_ne_id'] + self.slash + find['shelf_id'] + self.slash + find['slot_id']) == item['z_oa_fingerprint']:
                    input_Pm_find_z = find
                    break
            if input_Pm_find_a:
                a_power = input_Pm_find_a['in_power']
            if input_Pm_find_z:
                z_power = input_Pm_find_z['in_power']
            calc_Incomings.append({
                "source_oa_fingerprint": item['a_oa_fingerprint'],
                "source_power": a_power,
                "target_oa_fingerprint": item['z_oa_fingerprint'],
                "target_power": z_power,
                "timestamp": item['timestamp'],
                "is_history": item['is_history']
            })
            calc_Incomings.append({
                "source_oa_fingerprint": item['z_oa_fingerprint'],
                "source_power": z_power,
                "target_oa_fingerprint": item['a_oa_fingerprint'],
                "target_power": a_power,
                "timestamp": item['timestamp'],
                "is_history": item['is_history']
            })
        
        calc_Incomings = list(set(calc_Incomings))
            
        for item in calc_Incomings:
            incoming_optical_power = 0
            internal_Voa = 0
            outside_voa = 0
            # oafingerprint = item['source_oa_fingerprint'].split(self.slash)
            internal_find = None
            for find in input_Voa_Configs:
                if (find['ne_id'] + self.slash + find['shelf_id'] + self.slash + find['slot_id']) == item['source_oa_fingerprint']:
                    internal_find = find
                    break
            if internal_find:
                internal_Voa = internal_find['voa_vaule']
            outside_find = None
            for find in input_Internal_Topologies:
                if ((find['a_ne_id'] + self.slash + find['a_shelf_id'] + self.slash + find['a_slot_id']) == item['source_oa_fingerprint'] and (find['z_board_model'].find("VA") >= 0 or find['z_board_model'].find("LAC") >= 0)) or \
                    ((find['z_ne_id'] + self.slash + find['z_shelf_id'] + self.slash + find['z_slot_id']) == item['source_oa_fingerprint'] and (find['a_board_model'].find("VA") >= 0 or find['a_board_model'].find("LAC") >=0 )):
                    outside_find = find
                    break
            if outside_find:
                ne_id = ""
                shelf_id = ""
                slot_id = ""
                port_id = ""
                if outside_find['a_board_model'].find("VA") >= 0 or outside_find['a_board_model'].find("LAC") >= 0:
                    ne_id = outside_find['a_ne_id']
                    shelf_id = outside_find['a_shelf_id']
                    slot_id = outside_find['a_slot_id']
                    port_id = outside_find['a_port_id']
                else:
                    ne_id = outside_find['z_ne_id']
                    shelf_id = outside_find['z_shelf_id']
                    slot_id = outside_find['z_slot_id']
                    port_id = outside_find['z_port_id']
                VA4 = None
                for find in input_Voa_Configs:
                    if find['ne_id'] == ne_id and find['shelf_id'] == shelf_id and find['slot_id'] == slot_id and find['port_id'] == port_id:
                        VA4 = find
                        break
                if VA4:
                    outside_voa = VA4['voa_vaule']
            if item['source_power'] != 0:
                incoming_optical_power = item['source_power'] + internal_Voa + outside_voa
            _Incoming_Optical.append({
                "oa_fingerprint": item['source_oa_fingerprint'],
                "incoming_optical_power": incoming_optical_power,
                "internal_voa": internal_Voa,
                "outside_voa": outside_voa,
                "timestamp": item['timestamp'],
                "is_history": 2
            })
        # ComputedMysqlExecuteHelper.Instance.setCalc_incoming_optical_powerAddRange(_Incoming_Optical);
        CalcIncomingOpticalPower.bulk_add(_Incoming_Optical)
                
    def ComputedCalc_oa_power(self):
        input_Pm_Datas = InputPmData.get(is_history=2)
        calc_Incoming = CalcIncomingOpticalPower.get(is_history=2)
        input_Voa_Back_Datas = InputVoaBackData.get(is_history=2)
        oa_Powers = []
        for item in calc_Incoming:
            oaArr = item['oa_fingerprint'].split(self.slash)
            ne_id = oaArr[0]
            shelf_id = oaArr[1]
            slot_id = oaArr[2]
            internal_voa = item['internal_voa']
            outside_voa = item['outside_voa']
            incoming_power = 0
            outing_power = 0
            is_voa_back = 0
            voa_Back_Data_find = None
            for find in input_Voa_Back_Datas:
                if find['ne_id'] == ne_id and find['shelf_id'] == shelf_id and find['slot_id'] == slot_id:
                    voa_Back_Data_find = find
                    break
            if voa_Back_Data_find:
                is_voa_back = voa_Back_Data_find['vo']
            pm_Data_find = None
            for find in input_Pm_Datas:
                if find['a_ne_id'] == ne_id and find['shelf_id'] == shelf_id and find['slot_id'] == slot_id:
                    pm_Data_find = find
                    break
            if pm_Data_find:
                if is_voa_back == 1:
                    incoming_power = pm_Data_find['in_power'] + outside_voa
                    outing_power = pm_Data_find['out_power'] - internal_voa
                else:
                    incoming_power = pm_Data_find['in_power'] + outside_voa + internal_voa
                    outing_power = pm_Data_find['out_power']
            oa_Powers.append({
                "source_ne_id": ne_id,
                "source_oa_shelf_id": shelf_id,
                "source_oa_slot_id": slot_id,
                "internal_voa": internal_voa,
                "outerside_voa": outside_voa,
                "incoming_power": incoming_power,
                "outing_power": outing_power,
                "is_voa_back": is_voa_back,
                "timestamp": item['timestamp'],
                "is_history": 2
            })
        CalcOaPower.bulk_add(oa_Powers)
        
    def ComputedCalc_ne_oas(self):
        data = InputTopologyData.get(is_history=2)
        calc_Ne_Oas = []
        calc_ne_oasP = []
        calc_ne_oasR = []
        pmDataIncomings = getPmDataIncomingPower()
        calc_Oa_Powers = CalcOaPower.get(is_history=2)
        
        for item in data:
            source_ne_id = item['a_ne_id']
            source_oa_sub_name = item['a_sub_name']
            source_oa_shelf_id = item['a_shelf_id']
            source_oa_slot_id = item['a_slot_id']
            source_oa_in_out_id = item['a_in_out_id']
            target_ne_id = item['z_ne_id']
            target_oa_sub_name = item['z_sub_name']
            target_oa_shelf_id = item['z_shelf_id']
            target_oa_slot_id = item['z_slot_id']
            target_oa_in_out_id = item['z_in_out_id']
            source_oa_fingerprint = source_ne_id + self.slash + source_oa_shelf_id + self.slash + \
                source_oa_slot_id
            source_oa_dir_fingerprint = source_ne_id + self.slash + source_oa_shelf_id + \
                self.slash + source_oa_slot_id + self.slash + source_oa_in_out_id
            target_oa_fingerprint = target_ne_id + self.slash + target_oa_shelf_id + \
                self.slash + target_oa_slot_id
            target_oa_dir_fingerprint = target_ne_id + self.slash + target_oa_shelf_id + \
                self.slash + target_oa_slot_id + self.slash + target_oa_in_out_id
            act_stand = item['act_stand']
            full_waves = item['full_waves']
            timestamp = item['timestamp']
            fiber_loss = 0
            oa_out_Power = None
            oa_in_Power = None
            if source_oa_in_out_id == self.send:
                for find in calc_Oa_Powers:
                    if find['source_ne_id'] == target_ne_id and find['source_oa_shelf_id'] == target_oa_shelf_id and find['source_oa_slot_id'] == target_oa_slot_id:
                        oa_out_Power = find
                        break
                for find in calc_Oa_Powers:
                    if find['source_ne_id'] == target_ne_id and find['source_oa_shelf_id'] == target_oa_shelf_id and find['source_oa_slot_id'] == target_oa_slot_id:
                        oa_in_Power = find
                        break
            else:
                for find in calc_Oa_Powers:
                    if find['source_ne_id'] == target_ne_id and find['source_oa_shelf_id'] == target_oa_shelf_id and find['source_oa_slot_id'] == target_oa_slot_id:
                        oa_out_Power = find
                        break
                for find in calc_Oa_Powers:
                    if find['source_ne_id'] == source_ne_id and find['source_oa_shelf_id'] == source_oa_shelf_id and find['source_oa_slot_id'] == source_oa_slot_id:
                        oa_in_Power = find
                        break
            if oa_out_Power and oa_in_Power:
                result = oa_out_Power['outing_power'] - oa_in_Power['incoming_power']
                fiber_loss = result if result <= 2 else abs(result) - 2
            
            calc_ne_oasP.append({
                "source_ne_id": source_ne_id,
                "source_oa_sub_name": source_oa_sub_name,
                "source_oa_shelf_id": source_oa_shelf_id,
                "source_oa_slot_id": source_oa_slot_id,
                "source_oa_in_out_id": source_oa_in_out_id,
                "source_oa_fingerprint": source_oa_fingerprint,
                "source_oa_dir_fingerprint": source_oa_dir_fingerprint,
                "target_ne_id": target_ne_id,
                "target_oa_sub_name": target_oa_sub_name,
                "target_oa_shelf_id": target_oa_shelf_id,
                "target_oa_slot_id": target_oa_slot_id,
                "target_oa_in_out_id": target_oa_in_out_id,
                "target_oa_fingerprint": target_oa_fingerprint,
                "target_oa_dir_fingerprint": target_oa_dir_fingerprint,
                "act_stand": act_stand,
                "full_waves": full_waves,
                "fiber_loss": fiber_loss,
                "timestamp": timestamp,
                "is_history": 2
            })
            calc_ne_oasR.append({
                "source_ne_id": target_ne_id,
                "source_oa_sub_name": target_oa_sub_name,
                "source_oa_shelf_id": target_oa_shelf_id,
                "source_oa_slot_id": target_oa_slot_id,
                "source_oa_in_out_id": target_oa_in_out_id,
                "source_oa_fingerprint": target_oa_fingerprint,
                "source_oa_dir_fingerprint": target_oa_dir_fingerprint,
                "target_ne_id": source_ne_id,
                "target_oa_sub_name": source_oa_sub_name,
                "target_oa_shelf_id": source_oa_shelf_id,
                "target_oa_slot_id": source_oa_slot_id,
                "target_oa_in_out_id": source_oa_in_out_id,
                "target_oa_fingerprint": source_oa_fingerprint,
                "target_oa_dir_fingerprint": source_oa_dir_fingerprint,
                "act_stand": act_stand,
                "full_waves": full_waves,
                "fiber_loss": fiber_loss,
                "timestamp": timestamp,
                "is_history": 2
            })
            
            for item in calc_ne_oasP:
                calc_find = None
                for find in calc_Ne_Oas:
                    if find['source_oa_dir_fingerprint'] == item['source_oa_dir_fingerprint']:
                        calc_find = find
                        break
                if calc_find is None:
                    calc_Ne_Oas.append(item)
            
            for item in calc_ne_oasR:
                calc_find = None
                for find in calc_Ne_Oas:
                    if find['source_oa_dir_fingerprint'] == item['source_oa_dir_fingerprint']:
                        calc_find = find
                        break
                if calc_find is None:
                    calc_Ne_Oas.append(item)
        CalcNeOas.bulk_add(calc_Ne_Oas)

    def ComputedCalc_ola_Business_waves(self):
        calc_Oms = CalcOms.get(is_history=2)
        calc_adj = CalcNeAdj.get(is_history=2)
        input_optical_ne = InputOpticalNe.get(is_history=2)
        source_ola = []
        target_ola = []
        ola_Business_Waves = []
        source_ola = list(filter(lambda item: item['source_ne_type'].find('OLA') >= 0, calc_adj))
        target_ola = list(filter(lambda item: item['target_ne_type'].find('OLA') >= 0, calc_adj))
        for item in source_ola:
            ne_id = item['source_ne_id']
            oms_source_id = ""
            oms_target_id = ""
            oms_source_sub_name = ""
            oms_target_sub_name = ""
            business_waves = 0
            oms = None
            for o in calc_Oms:
                if o['ola_all'].find(ne_id) >= 0:
                    oms = o
                    break
            if oms:
                oms_source_id = oms['oms_source_id']
                oms_target_id = oms['oms_target_id']
                business_waves = oms['business_waves']
                source = None
                target = None
                for find in input_optical_ne:
                    if find['ne_id'] == oms_source_id:
                        source = find
                        break
                for find in input_optical_ne:
                    if find['ne_id'] == oms_target_id:
                        target = find
                        break
                if source:
                    oms_source_sub_name = source['ne_name']
                if target:
                    oms_target_sub_name = target['ne_name']
                ola_Business_Waves.append({
                    "ola_ne_id": ne_id,
                    "business_waves": business_waves,
                    "oms_source_id": oms_source_id,
                    "oms_target_id": oms_target_id,
                    "oms_source_sub_name": oms_source_sub_name,
                    "oms_target_sub_name": oms_target_sub_name,
                    "sys_name": item['sys_name'],
                    "timestamp": item['timestamp'],
                    "is_history": 2
                })
        for item in target_ola:
            ne_id = item['target_ne_id']
            oms_source_id = ""
            oms_target_id = ""
            oms_source_sub_name = ""
            oms_target_sub_name = ""
            business_waves = 0
            oms =None
            for o in calc_Oms:
                if o['ola_all'].find(ne_id) >= 0:
                    oms = o
                    break
            if oms:
                oms_source_id = oms['oms_source_id']
                oms_target_id = oms['oms_target_id']
                business_waves = oms['business_waves']
                source = None
                target = None
                for item in calc_adj:
                    if item['source_ne_id'] == oms_source_id:
                        source = item
                        break
                for item in calc_adj:
                    if item['target_ne_id'] == oms_target_id:
                        target = item
                        break
                if source:
                    oms_source_sub_name = source['source_sub_name']
                if target:
                    oms_target_sub_name = target['target_sub_name']
                ola_Business_Waves.append({
                    "ola_ne_id": ne_id,
                    "business_waves": business_waves,
                    "oms_source_id": oms_source_id,
                    "oms_target_id": oms_target_id,
                    "oms_source_sub_name": oms_source_sub_name,
                    "oms_target_sub_name": oms_target_sub_name,
                    "sys_name": item['sys_name'],
                    "timestamp": item['timestamp'],
                    "is_history": 2
                })
        ola_Business_Waves = list(set(ola_Business_Waves))
        CalcOlaBusinessWaves.bulk_add(ola_Business_Waves)
    
    def _otmOadmCheck(self, ne_type):
        if ne_type.find(self.siteOTM) >=0 or ne_type.find(self.siteROADM) >=0:
            return True
        return False
    
    def ComputedCalc_otm_bussiness_waves(self):
        calc_Ne_Oas = CalcNeOas.get(is_history=2)
        input_Optical_Nes = InputOpticalNe.get(is_history=2)
        input_Opticals_OTM_OADM = list(filter(lambda x : self._otmOadmCheck(x['ne_type']), input_Optical_Nes))
        _Business_Waves = []
        _Oms = CalcOms.get(is_history=2)
        for item in calc_Ne_Oas:
            source_ne_id = item['source_ne_id']
            source_oa_in_out_id = ""
            source_ne_type = ne_typeFind(input_Opticals_OTM_OADM, source_ne_id)
            oms_source_id = ""
            oms_source_sub_name = ""
            target_ne_id = item['target_ne_id']
            target_oa_in_out_id = ""
            target_ne_type = ne_typeFind(input_Opticals_OTM_OADM, target_ne_id)
            oms_target_id = ""
            oms_target_sub_name = ""
            sys_name = ""
            business_waves = 0
            
            if not self._otmOadmCheck(source_ne_type):
                return
            oms = omsFind(_Oms, self._otmOadmCheck(target_ne_type), target_ne_id, source_ne_id)
            
            if oms:
                oms_source_id = oms.oms_source_id
                oms_target_id = oms.oms_target_id
                business_waves = oms.business_waves
                sys_name = oms.sys_name
                source = _optical_neFind(input_Optical_Nes, oms_source_id)
                target = _optical_neFind(input_Optical_Nes, oms_target_id)
                if source:
                    oms_source_sub_name = source['ne_name']
                if target:
                    oms_target_sub_name = target['ne_name']
            
            _Business_Waves.append({
                "source_ne_id": source_ne_id,
                "source_oa_shelf_id": item.source_oa_shelf_id,
                "source_oa_slot_id": item.source_oa_slot_id,
                "source_oa_fingerprint": item.source_oa_fingerprint,
                "target_ne_id": target_ne_id,
                "target_oa_shelf_id": item.target_oa_shelf_id,
                "target_oa_slot_id": item.target_oa_slot_id,
                "target_oa_fingerprint": item.source_oa_fingerprint,
                "business_waves": business_waves,
                "oms_source_id": oms_source_id,
                "oms_target_id": oms_target_id,
                "oms_source_sub_name": oms_source_sub_name,
                "oms_target_sub_name": oms_target_sub_name,
                "sys_name": sys_name,
                "timestamp": item.timestamp,
                "is_history": 2
            })
        CalcOtmBusinessWaves.bulk_add(_Business_Waves)

    def ComputedCalc_oa_stand(self):
        calc_sGroup = getCalc_ne_oasGroup()
        _Board_Types = InputOaBoardType.get_input_oa_board_types(is_history=2)
        _Board_Standards = InputOaBoardStandard.get_input_oa_board_standards(is_history=2)
        _ola_Business_Waves = CalcOlaBusinessWaves.get(is_history=2)
        _otm_Business_Waves = CalcOtmBusinessWaves.get(is_history=2)
        oa_Stands = []
        for item in calc_sGroup:
            standard_gain_min = 0
            standard_gain_max = 0
            standard_wave_output = 0
            single_wave_output = 0
            business_waves = 0
            input_Oa_find = None
            for find in _Board_Types:
                if (find['ne_id'] + "/" + find['shelf_id'] + "/" + find['slot_id']) == item['source_oa_fingerprint']:
                    input_Oa_find = find
                    break
            if input_Oa_find:
                _Board_Standard_find = next(
                    filter(lambda find: find['board_model'] == input_Oa_find['board_model'],
                           _Board_Standards), None)
                if _Board_Standard_find:
                    standard_gain_min = _Board_Standard_find['standard_gain_min']
                    standard_gain_max = _Board_Standard_find['standard_gain_max']
                    match item['full_waves']:
                        case 40:
                            single_wave_output = _Board_Standard_find['standard_single_40_wave_output']
                        case 80:
                            single_wave_output = _Board_Standard_find['standard_single_80_wave_output']
                        case 96:
                            single_wave_output = _Board_Standard_find['standard_single_96_wave_output']
            calc_Ola_find = None
            for find in _ola_Business_Waves:
                if find['ola_ne_id'] == item['source_ne_id']:
                    calc_Ola_find = find
                    break
            if calc_Ola_find:
                business_waves = calc_Ola_find['business_waves']
            else:
                calc_Otm_find = None
                for find in _otm_Business_Waves:
                    if find['source_oa_fingerprint'] == item['source_oa_fingerprint']:
                        calc_Otm_find = find
                        break
                if calc_Otm_find:
                    business_waves = calc_Otm_find['business_waves']
            
            if business_waves != 0:
                standard_wave_output = single_wave_output + (10 * math.log10(business_waves))
            oa_Stands.append({
                "oa_fingerprint": item['source_oa_fingerprint'],
                "standard_gain_min": standard_gain_min,
                "standard_gain_max": standard_gain_max,
                "standard_wave_output": standard_wave_output,
                "timestamp": item['timestamp'],
                "is_history": 2
            })
        # ComputedMysqlExecuteHelper.Instance.setCalc_oa_standAddRange(oa_Stands);
        CalcOaStand.bulk_add(oa_Stands)
    
    def ComputedRisk_fiber(self):
        dataRisk_fiber = getComRisk_fiber()
        input_Stds = InputStdValues.get_input_std_values(is_history=2)
        input_Thresholds = InputThreshold.get_input_thresholds(is_history=2)
        risk_Fibers = []
        for item in dataRisk_fiber:
            is_risk = ""
            is_emergency = ""
            net_level = item["network_level"]
            city = item["city"]
            fiber_two_way_dev_risk = 0
            fiber_lossOne = 0
            fiber_lossTwo = 0
            cable_in_out_baseline = input_Stds[0]['cable_in_out_baseline'] if len(input_Stds) > 0 else 0
            fiber_lossArr = [float(x) for x in item["fiber_lossArr"].split(',')]
            findThreshold = Input_thresholdFind(input_Thresholds, city, net_level)
            manual_cable_in_out_baseline = float(item["manual_cable_in_out_baseline"])
            manual_cableCom = cable_in_out_baseline if manual_cable_in_out_baseline == 0.00 else manual_cable_in_out_baseline
            if len(fiber_lossArr) >= 2:
                fiber_lossOne = fiber_lossArr[0]
                fiber_lossTwo = fiber_lossArr[1]
                fiber_two_way_dev_risk = abs(fiber_lossOne - fiber_lossTwo)
                if fiber_lossOne == 0 or fiber_lossTwo == 0:
                    is_risk = self.ok
                    is_emergency = self.er_ok
                else:
                    is_risk = "high" if (fiber_two_way_dev_risk - manual_cableCom > findThreshold['fiber_two_way_dev_risk_thr']) else self.ok
                    is_emergency = "higher" if (fiber_two_way_dev_risk - manual_cableCom > findThreshold['fiber_two_way_dev_risk_urg']) else self.er_ok
            else:
                fiber_lossOne = fiber_lossArr[0]
                if fiber_lossOne == 0:
                    is_risk = self.ok
                    is_emergency = self.er_ok
                else:
                    is_risk = "high" if (fiber_two_way_dev_risk - manual_cableCom > findThreshold['fiber_two_way_dev_risk_thr']) else self.ok
                    is_emergency = "higher" if (fiber_two_way_dev_risk - manual_cableCom > findThreshold.fiber_two_way_dev_risk_urg) else self.er_ok
            risk_Fibers.append({
                "source_ne_id": item['source_ne_id'],
                "target_ne_id": item['target_ne_id'],
                "act_stand": item['act_stand'],
                "fiber_loss_1": fiber_lossOne,
                "fiber_loss_2": fiber_lossTwo,
                "fiber_two_way_dev_risk": fiber_two_way_dev_risk,
                "cable_in_out_baseline": manual_cableCom,
                "is_risk": is_risk,
                "is_emergency": is_emergency,
                "city": city,
                "net_level": net_level,
                "timestamp": item['timestamp'],
                "is_history": 2
            })
        RiskFiber.bulk_add(risk_Fibers)
        
    def ComputedRisk_olp(self):
        input_Internal_s = getInput_internal_topologyOLP()
        input_Thresholds = getInput_thresholdCopy()
        input_Optical_Nes = InputOpticalNe.get(is_history=2)
        top_Olps = TopOlp.all()
        std_Values = InputStdValues.get_input_std_values(is_history=2)
        input_Tp_data = InputTopologyData.get(is_history=2)
        calc_Oa_Powers = CalcOaPower.get(is_history=2)
        risk_olps = []
        for item in input_Internal_s:
            oa_ne_id_1 = ""
            oa_shelf_id_1 = ""
            oa_slot_id_1 = ""
            oa_ne_id_2 = ""
            oa_shelf_id_2 = ""
            oa_slot_id_2 = ""
            olp_power_dev_risk = 0
            olp_act_stand_baseline = 0
            if item['a_board_model'].find("OLP") >= 0:
                city = None
                network_level = None
                input_a = list(filter(lambda x: (x['a_ne_id'] == item['a_ne_id'] and x['a_shelf_id'] == item['a_shelf_id'] and x['a_slot_id'] == item['a_slot_id']) or \
                    (x['z_ne_id'] == item['a_ne_id'] and x['z_shelf_id'] == item['a_shelf_id'] and x["z_slot_id"] == item['a_slot_id']), input_Internal_s))
                top_ = next(filter(lambda find: find['olp_ne_id'] == item['a_ne_id'] and find['olp_shelf_id'] == item['a_shelf_id'] and find['olp_slot_id'] == item['a_slot_id'], top_Olps), None)
                input_optical_neFind = next(filter(lambda find: find['ne_id'] == item['a_ne_id'], input_Optical_Nes), None)
                input_topology_dataFind = None
                if input_optical_neFind:
                    city = input_optical_neFind['city']
                    network_level = input_optical_neFind['network_level']
                else:
                    input_topology_dataFind = next(
                        filter(lambda find: find['a_ne_id'] == item['a_ne_id'] or \
                            find['z_ne_id'] == item['a_ne_id'], input_Tp_data), None)
                    if input_topology_dataFind:
                        city = input_optical_neFind['city']
                        network_level = input_optical_neFind['network_level']
                if city and network_level:
                    if len(input_a) == 1:
                        oa_1 = next((item for item in input_a), None)
                        oa_1_check = "OAU" in oa_1["a_board_model"] if oa_1 else False
                        oa_ne_id_1 = oa_1["a_ne_id"] if oa_1_check else oa_1["z_ne_id"]
                        oa_shelf_id_1 = oa_1["a_shelf_id"] if oa_1_check else oa_1["z_shelf_id"]
                        oa_slot_id_1 = oa_1["a_slot_id"] if oa_1_check else oa_1["z_slot_id"]
                    else:
                        oa_1 = next((item for item in input_a), None)
                        oa_2 = next((item for item in reversed(input_a)), None)
                        oa_1_check = "OAU" in oa_1["a_board_model"] if oa_1 else False
                        oa_2_check = "OAU" in oa_2["a_board_model"] if oa_2 else False
                        oa_ne_id_1 = oa_1["a_ne_id"] if oa_1_check else oa_1["z_ne_id"]
                        oa_shelf_id_1 = oa_1["a_shelf_id"] if oa_1_check else oa_1["z_shelf_id"]
                        oa_slot_id_1 = oa_1["a_slot_id"] if oa_1_check else oa_1["z_slot_id"]
                        oa_ne_id_2 = oa_2["a_ne_id"] if oa_2_check else oa_2["z_ne_id"]
                        oa_shelf_id_2 = oa_2["a_shelf_id"] if oa_2_check else oa_2["z_shelf_id"]
                        oa_slot_id_2 = oa_2["a_slot_id"] if oa_2_check else oa_2["z_slot_id"]

                        oa_Power1 = next((find for find in calc_Oa_Powers if find["source_ne_id"] == item["a_ne_id"] and find["source_oa_shelf_id"] == oa_shelf_id_1 and find["source_oa_slot_id"] == oa_slot_id_1), None)
                        oa_Power2 = next((find for find in calc_Oa_Powers if find["source_ne_id"] == item["a_ne_id"] and find["source_oa_shelf_id"] == oa_shelf_id_2 and find["source_oa_slot_id"] == oa_slot_id_2), None)

                        if oa_Power1 is not None and oa_Power2 is not None:
                            olp_power_dev_risk = abs(oa_Power1["outing_power"] - oa_Power2["outing_power"])
                    
                    if top_ is None:
                        olp_act_stand_baseline = std_Values[0]['olp_act_stand_baseline'] if len(std_Values) > 0 else 0
                    else:
                        olp_act_stand_baseline = top_["manual_olp_act_stand_baseline"]
                    input_ = Input_thresholdFind(input_Thresholds, city, network_level)
                    risk_olps.append({
                            "olp_ne_id": item['a_ne_id'],
                            "olp_shelf_id": item['a_shelf_id'],
                            "olp_slot_id": item['a_slot_id'],
                            "oa_ne_id_1": oa_ne_id_1,
                            "oa_shelf_id_1": oa_shelf_id_1,
                            "oa_slot_id_1": oa_slot_id_1,
                            "oa_ne_id_2": oa_ne_id_2,
                            "oa_shelf_id_2": oa_shelf_id_2,
                            "oa_slot_id_2": oa_slot_id_2,
                            "olp_power_dev_risk": olp_power_dev_risk,
                            "olp_act_stand_baseline": olp_act_stand_baseline,
                            "is_risk": "high" if (olp_power_dev_risk - olp_act_stand_baseline) > input_['olp_power_dev_risk_thr'] else self.ok,
                            "is_emergency": "higher" if (olp_power_dev_risk - olp_act_stand_baseline) > input_['olp_power_dev_risk_urg'] else self.er_ok,
                            "city": city,
                            "net_level": network_level,
                            "timestamp": item['timestamp'],
                            "is_history": 2
                    })
        else:
            city = ""
            network_level = ""
            input_b = next(
                filter(lambda find: find['olp_ne_id'] == item['z_ne_id'] and \
                    find['olp_shelf_id'] == item['z_shelf_id'] and \
                        find['olp_slot_id'] == item['z_slot_id'], top_Olps), None)
            top_ = next(
                filter(lambda find: find['olp_ne_id'] == item['z_ne_id'] and \
                    find['olp_shelf_id'] == item['z_shelf_id'] and \
                        find['olp_slot_id'] == item['z_slot_id'], top_Olps), None)
            input_optical_neFind = next(
                filter(lambda find: find['ne_id'] == item['z_ne_id'], input_Optical_Nes), None)
            input_topology_dataFind = None
            if input_optical_neFind:
                city = input_optical_neFind['city']
                network_level = input_optical_neFind['network_level']
            else:
                input_topology_dataFind = next(
                    filter(lambda find: find['a_ne_id'] == item['a_ne_id'] or \
                        find['z_ne_id'] == item['a_ne_id'], input_Tp_data), None)
                if input_topology_dataFind:
                    city = input_topology_dataFind['city']
                    network_level = input_topology_dataFind['net_level']
            if city and network_level:
                if len(input_b) <= 1:
                    oa_1 = input_b[0] if input_b else None
                    oa_1_check = "OAU" in oa_1["a_board_model"] if oa_1 else False
                    oa_ne_id_1 = oa_1["a_ne_id"] if oa_1_check else oa_1["z_ne_id"]
                    oa_shelf_id_1 = oa_1["a_shelf_id"] if oa_1_check else oa_1["z_shelf_id"]
                    oa_slot_id_1 = oa_1["a_slot_id"] if oa_1_check else oa_1["z_slot_id"]
                else:
                    oa_1 = next((item for item in input_b), None)
                    oa_2 = next((item for item in reversed(input_b)), None)
                    oa_1_check = "OAU" in oa_1["a_board_model"] if oa_1 else False
                    oa_2_check = "OAU" in oa_2["a_board_model"] if oa_2 else False
                    oa_ne_id_1 = oa_1["a_ne_id"] if oa_1_check else oa_1["z_ne_id"]
                    oa_shelf_id_1 = oa_1["a_shelf_id"] if oa_1_check else oa_1["z_shelf_id"]
                    oa_slot_id_1 = oa_1["a_slot_id"] if oa_1_check else oa_1["z_slot_id"]
                    oa_ne_id_2 = oa_2["a_ne_id"] if oa_2_check else oa_2["z_ne_id"]
                    oa_shelf_id_2 = oa_2["a_shelf_id"] if oa_2_check else oa_2["z_shelf_id"]
                    oa_slot_id_2 = oa_2["a_slot_id"] if oa_2_check else oa_2["z_slot_id"]

                    oa_Power1 = next((find for find in calc_Oa_Powers if find["source_ne_id"] == item["z_ne_id"] and find["source_oa_shelf_id"] == oa_shelf_id_1 and find["source_oa_slot_id"] == oa_slot_id_1), None)
                    oa_Power2 = next((find for find in calc_Oa_Powers if find["source_ne_id"] == item["z_ne_id"] and find["source_oa_shelf_id"] == oa_shelf_id_2 and find["source_oa_slot_id"] == oa_slot_id_2), None)

                    if oa_Power1 is not None and oa_Power2 is not None:
                        olp_power_dev_risk = abs(oa_Power1["outing_power"] - oa_Power2["outing_power"])
                if top_ is None:
                    olp_act_stand_baseline = std_Values[0]["olp_act_stand_baseline"] if std_Values else None
                else:
                    olp_act_stand_baseline = top_["manual_olp_act_stand_baseline"]
                input_ = Input_thresholdFind(input_Thresholds, city, network_level)
                risk_olps.append({
                    "olp_ne_id": item['z_ne_id'],
                    "olp_shelf_id": item['z_shelf_id'],
                    "olp_slot_id": item['z_slot_id'],
                    "oa_ne_id_1": oa_ne_id_1,
                    "oa_shelf_id_1": oa_shelf_id_1,
                    "oa_slot_id_1": oa_slot_id_1,
                    "oa_ne_id_2": oa_ne_id_2,
                    "oa_shelf_id_2": oa_shelf_id_2,
                    "oa_slot_id_2": oa_slot_id_2,
                    "olp_power_dev_risk": olp_power_dev_risk,
                    "olp_act_stand_baseline": olp_act_stand_baseline,
                    "is_risk": "high" if (olp_power_dev_risk - olp_act_stand_baseline) > input_['olp_power_dev_risk_thr'] else self.ok,
                    "is_emergency": "higher" if (olp_power_dev_risk - olp_act_stand_baseline) > input_.olp_power_dev_risk_urg else self.er_ok,
                    "city": city,
                    "net_level": network_level,
                    "timestamp": item['timestamp'],
                    "is_history": 2
                })
        risk_olps = list(set(risk_olps))
        RiskOlp.bulk_add(risk_olps)

    def ComputedRisk_oa(self):
        data_calc_ne_oas = CalcNeOas.get(is_history=2)
        risk_Oas = []
        data_input_optical_ne = InputOpticalNe.get(is_history=2)
        data_input_pm_data = InputPmData.get(is_history=2)
        data_input_threshold = InputThreshold.get_input_thresholds(is_history=2)
        data_input_std_values = InputStdValues.get_input_std_values(is_history=2)
        data_calc_oa_stand = CalcOaStand.get(is_history=2)
        data_top_power_max_min = TopPowerMaxMin.get(is_history=2)
        data_top_gain = TopGain.get(is_history=2)
        data_top_oa_stand = TopOaStand.get(is_history=2)
        
        std_optical_power_baseline = next((item for item in data_input_std_values), None)['optical_power_baseline'] \
            if len(data_input_std_values) > 0 else 0
        std_gain_baseline = next((item for item in data_input_std_values), None)['gain_baseline'] \
            if len(data_input_std_values) > 0 else 0
        for item in data_calc_ne_oas:
            source_ne_id = item['source_ne_id']
            source_shelf_id = item['source_oa_shelf_id']
            source_slot_id = item['source_oa_slot_id']
            city = ""
            net_level = ""
            input_Optical_Ne_find = next(filter(lambda find: find['ne_id'] == source_ne_id, data_input_optical_ne), None)
            if input_Optical_Ne_find:
                city = input_Optical_Ne_find['city']
                net_level = input_Optical_Ne_find['network_level']
            obj_risk_oa = {
                "city": city,
                "net_level": net_level,
                "source_ne_id": source_ne_id,
                "source_oa_shelf_id": source_shelf_id,
                "source_oa_slot_id": source_slot_id,
                "timestamp": item['timestamp'],
                "is_history": 2
            }
            input_Pm_Data_find = next(filter(lambda find: find.a_ne_id == source_ne_id and \
                find['shelf_id'] == source_shelf_id and find['slot_id'] == source_slot_id, data_input_pm_data), None)
            power = next(
                filter(lambda item: item['source_ne_id'] == source_ne_id and item['source_oa_shelf_id'] == source_shelf_id and \
                    item['source_oa_slot_id'] == source_slot_id, data_top_power_max_min), None)
            input_Threshold = Input_thresholdFind(data_input_threshold, city, net_level)
            top_gain = next(
                filter(lambda item: item['source_ne_id'] == source_ne_id and item['source_oa_shelf_id'] == source_shelf_id and \
                    item['source_oa_slot_id'] == source_slot_id, data_top_gain), None)
            top_oa = next(
                filter(lambda item: item['oa_fingerprint'] == (source_ne_id + self.slash + source_shelf_id + self.slash + source_slot_id), data_top_oa_stand), None)
            calc_Oa_Stand_find = next(
                filter(lambda item: item['oa_fingerprint'] == (source_ne_id + self.slash + source_shelf_id + self.slash + source_slot_id), data_calc_oa_stand), None)
            optical_power_baseline = power['manual_optical_power_baseline'] if power else std_optical_power_baseline
            gain_baseline = std_gain_baseline if top_gain is None else top_gain['manual_gain_baseline']
            
            if input_Pm_Data_find:
                obj_risk_oa = self.computed_input_Pm_Data_find(
                    input_Pm_Data_find, power, input_Threshold, top_gain, top_oa, calc_Oa_Stand_find,
                    optical_power_baseline, gain_baseline, obj_risk_oa)
            else:
                obj_risk_oa = self.computed_input_Pm_Data_not_find(
                    power, input_Threshold, top_gain, top_oa, calc_Oa_Stand_find,
                    optical_power_baseline, gain_baseline, obj_risk_oa)
            risk_Oas.append(obj_risk_oa)
        risk_Oas = list(set(risk_Oas))
        RiskOa.bulk_add(risk_Oas)

    def Risk_oa_summaryAdd(item):
        return {
            "city": item['city'],
            "net_level": item['net_level'],
            "source_ne_id": item['source_ne_id'],
            "source_oa_shelf_id": item['source_oa_shelf_id'],
            "source_oa_slot_id": item['source_oa_slot_id'],
            "oa_output_power_std_dev_risk": item['oa_output_power_std_dev_risk'],
            "standard_wave_output": item['standard_wave_output'],
            "is_output_power_dev_risk": item['is_output_power_dev_risk'],
            "is_output_power_dev_emergency": item['is_output_power_dev_emergency'],
            "timestamp": item['timestamp'],
            "is_history": 2
        }

    def ComputedRisk_oa_summary(self):
        _Ne_Oas = CalcNeOas.get(is_history=2)
        risk_s = RiskOa.get(is_history=2)
        risks_NoOK = list(filter(lambda item: item['is_output_power_dev_risk'] != self.ok, risk_s))
        oa_Summaries = []
        for item in risks_NoOK:
            calc_find = next(
                filter(lambda find: find['source_ne_id'] == item['source_ne_id'] and \
                    find['source_oa_shelf_id'] == item['source_oa_shelf_id'] and \
                        find['source_oa_slot_id'] == item['source_oa_slot_id'] and \
                            find['source_oa_in_out_id'] == self.put, _Ne_Oas), None)
            if calc_find is None:
                oa_Summaries.append(self.Risk_oa_summaryAdd(item))
        RiskOaSummary.bulk_add(oa_Summaries)
        
    def ComputedOrder_list(self):
        risk_Oas = RiskOa.get(is_history=2)
        input_Optical_Nes = InputOpticalNe.get(is_history=2)
        calc_Ne_Adjs = InputTopologyData.get(is_history=2)
        calc_ne_oas = CalcNeOas.get(is_history=2)
        calc_Ola_Business_Waves = CalcOlaBusinessWaves.get(is_history=2)
        calc_Otm_Business_Waves = CalcOtmBusinessWaves.get(is_history=2)
        risk_Oa_Summaries = RiskOaSummary.get_all_except({"is_output_power_dev_risk": 'ok'}, is_history=2)
        risk_Fibers = RiskFiber.get_all_except({"is_output_power_dev_risk": 'ok'}, is_history=2)
        risk_Olps = RiskOlp.get_all_except({"is_output_power_dev_risk": 'ok'}, is_history=2)
        old_order_list = OrderList.all()
        risk_Oas_is_input_power_fluc_risk = list(filter(lambda find: find['is_input_power_fluc_risk'] != self.ok, risk_Oas))
        risk_Oas_is_output_power_fluc_risk = list(filter(lambda find: find['is_output_power_fluc_risk'] != self.ok, risk_Oas))
        risk_Oas_is_gain_risk = list(filter(lambda find: find['is_gain_risk'] != self.ok, risk_Oas))
        order_Lists = []
        
        for item in risk_Fibers:
            source_ne_id = item['source_ne_id']
            target_ne_id = item['target_ne_id']
            source_shelf_id = "NULL"
            source_slot_id = "NULL"
            risk_level = "一般" if item['is_emergency'] == self.er_ok else "紧急"
            risk_type = "光缆损耗双向偏差超标"
            oms_source_sub_name = None
            oms_target_sub_name = None
            sys_name = None
            source_ne_name = ""
            target_ne_name = ""
            district_county = ""
            manufactor = ""
            
            input_find = next(filter(lambda find: find['ne_id'] == source_ne_id, input_Optical_Nes), None)
            if input_find:
                district_county = input_find['district_county']
                manufactor = input_find['manufactor']
            calc_Ola_find=next(
                filter(lambda find: find['ola_ne_id'] == item['source_ne_id'] or \
                    find['ola_ne_id'] == item['target_ne_id'], calc_Ola_Business_Waves), None)
            calc_find_source = next(
                filter(lambda find: find['source_ne_id'] == source_ne_id or \
                    find['target_ne_id'] == source_ne_id, calc_Ne_Adjs), None)
            calc_find_target = next(
                filter(lambda find: find['source_ne_id'] == target_ne_id or \
                    find['target_ne_id'] == target_ne_id, calc_Ne_Adjs), None)
            if calc_find_source:
                sys_name = calc_find_source["sys_name"] if sys_name is None or sys_name.strip() == "" else sys_name
            if calc_find_target:
                sys_name = calc_find_target["sys_name"] if sys_name is None or sys_name.strip() == "" else sys_name
            source = next(filter(lambda find: find['source_ne_id'] == source_ne_id, calc_ne_oas), None)
            target = next(filter(lambda find: find['source_ne_id'] == target_ne_id, calc_ne_oas), None)
            if source:
                source_ne_name = source['source_oa_sub_name']
            if target:
                target_ne_name = target['source_oa_sub_name']
            if calc_Ola_find:
                oms_source_sub_name = calc_Ola_find["oms_source_sub_name"]
                oms_target_sub_name = calc_Ola_find["oms_target_sub_name"]
            else:
                calc_Otm_find = next(
                    filter(lambda find: (find['source_ne_id'] == source_ne_id and find['target_ne_id'] == target_ne_id) or \
                        (find['source_ne_id'] == target_ne_id and find['target_ne_id'] == source_ne_id), calc_Otm_Business_Waves), None)
                if calc_Otm_find:
                    oms_source_sub_name = calc_Otm_find['oms_source_sub_name']
                    oms_target_sub_name = calc_Otm_find['oms_target_sub_name']
            if not source_ne_name and not target_ne_name and not sys_name:
                return
            risk_hash = Md5Generator.md5(item['source_ne_id'] + "--" + source_shelf_id + "--" + source_slot_id + "--" + item['target_ne_id'] + "--" + risk_type)
            old_order = next(
                filter(lambda find: find['risk_hash'] == risk_hash and find['is_top_end'] != 1, old_order_list), None)
            if old_order:
                return
            order_Lists.append({
                "risk_id": str(uuid.uuid4()),
                "risk_hash": risk_hash,
                "source_ne_id": item['source_ne_id'],
                "source_ne_sub_name": source_ne_name,
                "source_shelf_id": "",
                "source_slot_id": "",
                "target_ne_id": item['target_ne_id'],
                "target_ne_sub_name": target_ne_name,
                "city": item['city'],
                "district_county": district_county,
                "sys_name": sys_name,
                "oms": oms_source_sub_name + "--" + oms_target_sub_name + "--" + item['act_stand'],
                "network_level": item['net_level'],
                "manufactor": manufactor,
                "risk_level": risk_level,
                "risk_type": risk_type,
                "risk_content": source_ne_name + self.slash + target_ne_name + self.slash + risk_type,
                "current_value": item['fiber_two_way_dev_risk'],
                "standard_value": item['cable_in_out_baseline'],
                "unit_measurement": "dB",
                "discover_time": item['timestamp'],
                "is_send_top": 0,
                "is_top_end": 0,
                "timestamp": item['timestamp'],
                "is_history": 2
            })
        # risk_olp
        for item in risk_Olps:
            source_ne_id = item['olp_ne_id']
            source_shelf_id = item['olp_shelf_id']
            source_slot_id = item['olp_slot_id']
            source_ne_name = ""
            sys_name = ""
            risk_level = "一般" if item['is_emergency'] == self.er_ok else "紧急"
            risk_type = "OLP主备光功率偏差超标"
            district_county = ""
            manufactor = ""
            input_find = next(filter(lambda find: find['ne_id'] == source_ne_id, input_Optical_Nes), None)
            if input_find:
                district_county = input_find['district_county']
                manufactor = input_find['manufactor']
            calc_find = next(filter(lambda find: find['source_ne_id'] == source_ne_id or find['target_ne_id'] == source_ne_id, calc_Ne_Adjs), None)
            if calc_find:
                sys_name = calc_find['sys_name']
            source = next(filter(lambda find: find['source_ne_id'] == source_ne_id, calc_ne_oas), None)
            if source:
                source_ne_name = source['source_oa_sub_name']
            if not source_ne_name and not sys_name:
                return
            risk_hash = Md5Generator.md5(source_ne_id + "--" + source_shelf_id + "--" + source_slot_id + "--" + risk_type)
            old_order = next(filter(lambda find: find['risk_hash'] == risk_hash and find['is_top_end'] != 1, old_order_list), None)
            if old_order:
                return
            order_Lists.append({
                "risk_id": str(uuid.uuid4()),
                "risk_hash": risk_hash,
                "source_ne_id": item['olp_ne_id'],
                "source_ne_sub_name": source_ne_name,
                "source_shelf_id": item['olp_shelf_id'],
                "source_slot_id": item['olp_slot_id'],
                "target_ne_id": "",
                "target_ne_sub_name": "",
                "city": item['city'],
                "district_county": district_county,
                "sys_name": sys_name,
                "oms": "",
                "network_level": item['net_level'],
                "manufactor": manufactor,
                "risk_level": risk_level,
                "risk_type": risk_type,
                "risk_content": source_ne_name + self.slash + item['olp_shelf_id'] + self.slash + item['olp_slot_id'] + self.slash + risk_type,
                "current_value": item['olp_power_dev_risk'],
                "standard_value": item['olp_act_stand_baseline'],
                "unit_measurement": "dB",
                "discover_time": item['timestamp'],
                "is_send_top": 0,
                "is_top_end": 0,
                "timestamp": item['timestamp'],
                "is_history": 2
            })
        # risk_oa_is_input
        for item in risk_Oas_is_input_power_fluc_risk:
            source_ne_id = item['source_ne_id']
            source_shelf_id = item['source_oa_shelf_id']
            source_slot_id = item['source_oa_slot_id']
            risk_level = "一般" if item['is_input_power_fluc_emergency'] == self.er_ok else "紧急"
            risk_type = "输入光功率波动超标"
            oms_source_sub_name = None
            oms_target_sub_name = None
            sys_name = None
            source_ne_name = ""
            district_county = ""
            manufactor = ""
            
            input_find = next(filter(lambda find: find['ne_id'] == source_ne_id, input_Optical_Nes), None)
            if input_find:
                district_county = input_find['district_county']
                manufactor = input_find['manufactor']
            
            calc_find = next(filter(lambda find: find['source_ne_id'] == source_ne_id or find['target_ne_id'] == source_ne_id, calc_Ne_Adjs), None)
            if calc_find:
                sys_name = calc_find['sys_name']
            source = next(filter(lambda find: find['source_ne_id'] == source_ne_id, calc_ne_oas), None)
            if source:
                source_ne_name = source['source_oa_sub_name']
            calc_Ola_find = next(filter(lambda find: find['ola_ne_id'] == source_ne_id, calc_Ola_Business_Waves), None)
            if calc_Ola_find:
                oms_source_sub_name = calc_Ola_find['oms_source_sub_name']
                oms_target_sub_name = calc_Ola_find['oms_target_sub_name']
            else:
                calc_Otm_find = next(
                    filter(lambda find: (find['source_ne_id'] == source_ne_id and find['source_oa_shelf_id'] == source_shelf_id and find['source_oa_slot_id'] == source_slot_id) or \
                        (find['target_ne_id'] == source_ne_id and find['target_oa_shelf_id'] == source_shelf_id and find.target_oa_slot_id == source_slot_id), calc_Otm_Business_Waves), None)
                if calc_Otm_find:
                    oms_source_sub_name = calc_Otm_find['oms_source_sub_name']
                    oms_target_sub_name = calc_Otm_find['oms_target_sub_name']
            
            if not source_ne_name and not sys_name:
                return
            risk_hash = Md5Generator.md5(source_ne_id + "--" + source_shelf_id + "--" + source_slot_id + "--" + risk_type)
            old_order = next(filter(lambda find: find['risk_hash'] == risk_hash and find['is_top_end'] != 1, old_order_list), None)
            if old_order:
                return
            order_Lists.append({
                "risk_id": str(uuid.uuid4()),
                "risk_hash": risk_hash,
                "source_ne_id": source_ne_id,
                "source_ne_sub_name": source_ne_name,
                "source_shelf_id": source_shelf_id,
                "source_slot_id": source_slot_id,
                "target_ne_id": "",
                "target_ne_sub_name": "",
                "city": item['city'],
                "district_county": district_county,
                "sys_name": sys_name,
                "oms": oms_source_sub_name + self.slash + oms_target_sub_name,
                "network_level": item['net_level'],
                "manufactor": manufactor,
                "risk_level": risk_level,
                "risk_type": risk_type,
                "risk_content": source_ne_name + self.slash + source_shelf_id + self.slash + source_slot_id + self.slash + risk_type,
                "current_value": item['oa_input_power_fluc_risk'],
                'standard_value': item['optical_power_baseline'],
                "unit_measurement": "dB",
                "discover_time": item['timestamp'],
                "is_send_top": 0,
                "is_top_end": 0,
                "timestamp": item['timestamp'],
                "is_history": 2
            })
        # risk_oa_is_output
        for item in risk_Oas_is_output_power_fluc_risk:
            source_ne_id = item['source_ne_id']
            source_shelf_id = item['source_oa_shelf_id']
            source_slot_id = item['source_oa_slot_id']
            risk_level = "一般" if item['is_output_power_fluc_emergency'] == self.er_ok else "紧急"
            risk_type = "输出光功率波动超标"
            oms_source_sub_name = None
            oms_target_sub_name = None
            sys_name = None
            source_ne_name = ""
            district_county = ""
            manufactor = ""
            input_find = next(filter(lambda find: find['ne_id'] == source_ne_id, input_Optical_Nes), None)
            if input_find:
                district_county = input_find['district_county']
                manufactor = input_find['manufactor']
            calc_Ola_find = next(filter(lambda find: find['ola_ne_id'] == source_ne_id, calc_Ola_Business_Waves), None)
            calc_find = next(filter(lambda find: find['source_ne_id'] == source_ne_id or find['target_ne_id'] == source_ne_id, calc_Ne_Adjs), None)
            if calc_find:
                sys_name = calc_find['sys_name']
            source = next(filter(lambda find: find['source_ne_id'] == source_ne_id, calc_ne_oas), None)
            if source:
                source_ne_name = source['source_oa_sub_name']
            if calc_Ola_find:
                oms_source_sub_name = calc_Ola_find['oms_source_sub_name']
                oms_target_sub_name = calc_Ola_find['oms_target_sub_name']
            else:
                calc_Otm_find = next(
                    filter(lambda find: (find['source_ne_id'] == item['source_ne_id'] and find['source_oa_shelf_id'] == item['source_oa_shelf_id'] and \
                        find['source_oa_slot_id'] == item['source_oa_slot_id']) or (find['target_ne_id'] == item['source_ne_id'] and \
                            find['target_oa_shelf_id'] == item['source_oa_shelf_id'] and find['target_oa_slot_id'] == item['source_oa_slot_id']), calc_Otm_Business_Waves), None)
                if calc_Otm_find:
                    oms_source_sub_name = calc_Otm_find['oms_source_sub_name']
                    oms_target_sub_name = calc_Otm_find['oms_target_sub_name']
            
            if not source_ne_name and not sys_name:
                return
            risk_hash = Md5Generator.md5(source_ne_id + "--" + source_shelf_id + "--" + source_slot_id + "--" + risk_type)
            old_order = next(filter(lambda find: find['risk_hash'] == risk_hash and find['is_top_end'] != 1, old_order_list), None)
            if old_order:
                return
            order_Lists.append({
                "risk_id": str(uuid.uuid4()),
                "risk_hash": risk_hash,
                "source_ne_id": source_ne_id,
                "source_ne_sub_name": source_ne_name,
                "source_shelf_id": source_shelf_id,
                "source_slot_id": source_slot_id,
                "target_ne_id": "",
                "target_ne_sub_name": "",
                "city": item['city'],
                "district_county": district_county,
                "sys_name": sys_name,
                "oms": oms_source_sub_name + self.slash + oms_target_sub_name,
                "network_level": item['net_level'],
                "manufactor": manufactor,
                "risk_level": risk_level,
                "risk_type": risk_type,
                "risk_content": source_ne_name + self.slash + item['source_oa_shelf_id'] + self.slash + item['source_oa_slot_id'] + self.slash + risk_type,
                "current_value": item['oa_output_power_fluc_risk'],
                "standard_value": item['optical_power_baseline'],
                "unit_measurement": "dB",
                "discover_time": item['timestamp'],
                "is_send_top": 0,
                "is_top_end": 0,
                "timestamp": item['timestamp'],
                "is_history": 2
            })
        # risk_oa_is_gain_risk
        for item in risk_Oas_is_gain_risk:
            source_ne_id = item['source_ne_id']
            source_shelf_id = item['source_oa_shelf_id']
            source_slot_id = item['source_oa_slot_id']
            risk_level = "一般" if item['is_gain_emergency'] == self.er_ok else "紧急"
            risk_type = "光放板增益过高" if item['is_gain_risk'] == "high" else "光放板增益过低"
            oms_source_sub_name = None
            oms_target_sub_name = None
            sys_name = None
            source_ne_name = ""
            district_county = ""
            manufactor = ""
            
            input_find = next(filter(lambda find: find['ne_id'] == source_ne_id, input_Optical_Nes), None)
            if input_find:
                district_county = input_find['district_county']
                manufactor = input_find['manufactor']
            
            calc_Ola_find = next(filter(lambda find: find['ola_ne_id'] == source_ne_id, calc_Ola_Business_Waves), None)
            calc_find = next(filter(lambda find: find['source_ne_id'] == source_ne_id or find['target_ne_id'] == source_ne_id, calc_Ne_Adjs), None)
            if calc_find:
                sys_name = calc_find['sys_name']
            source = next(filter(lambda find: find['source_ne_id'] == source_ne_id, calc_ne_oas), None)
            if source:
                source_ne_name = source['source_oa_sub_name']
            if calc_Ola_find:
                oms_source_sub_name = calc_Ola_find['oms_source_sub_name']
                oms_target_sub_name = calc_Ola_find['oms_target_sub_name']
            else:
                calc_Otm_find = next(
                    filter(lambda find: (find['source_ne_id'] == item['source_ne_id'] and \
                        find['source_oa_shelf_id'] == item['source_oa_shelf_id'] and find['source_oa_slot_id'] == item['source_oa_slot_id']) or \
                            (find['target_ne_id'] == item['source_ne_id'] and find['target_oa_shelf_id'] == item['source_oa_shelf_id'] and \
                                find['target_oa_slot_id'] == item['source_oa_slot_id']), calc_Otm_Business_Waves), None)
                if calc_Otm_find:
                    oms_source_sub_name = calc_Otm_find['oms_source_sub_name']
                    oms_target_sub_name = calc_Otm_find['oms_target_sub_name']
            
            if not source_ne_name and not sys_name:
                return
            risk_hash = Md5Generator.md5(source_ne_id + "--" + source_shelf_id + "--" + source_slot_id + "--" + risk_type)
            old_order = next(filter(lambda find: find['risk_hash'] == risk_hash and find['is_top_end'] != 1, old_order_list), None)
            if old_order:
                return
            order_Lists.append({
                "risk_id": str(uuid.uuid4()),
                "risk_hash": risk_hash,
                "source_ne_id": source_ne_id,
                "source_ne_sub_name": source_ne_name,
                "source_shelf_id": source_shelf_id,
                "source_slot_id": source_slot_id,
                "target_ne_id": "",
                "target_ne_sub_name": "",
                "city": item['city'],
                "district_county": district_county,
                "sys_name": sys_name,
                "oms": oms_source_sub_name + self.slash + oms_target_sub_name,
                "network_level": item['net_level'],
                "manufactor": manufactor,
                "risk_level": risk_level,
                "risk_type": risk_type,
                "risk_content": source_ne_name + self.slash + item['source_oa_shelf_id'] + self.slash + item['source_oa_slot_id'] + self.slash + risk_type,
                "current_value": item['oa_gain_std_dev_risk'],
                "standard_value": item['gain_baseline'],
                "unit_measurement": "dB",
                "discover_time": item['timestamp'],
                "is_send_top": 0,
                "is_top_end": 0,
                "timestamp": item['timestamp'],
                "is_history": 2
            })
        # //risk_oa_summary
        for item in risk_Oa_Summaries:
            source_ne_id = item['source_ne_id']
            source_shelf_id = item['source_oa_shelf_id']
            source_slot_id = item['source_oa_slot_id']
            risk_level = "一般" if item['is_output_power_dev_emergency'] == er_ok else "紧急"
            risk_type = "光放板发光功率过高" if item['is_output_power_dev_risk'] == "high" else "光放板发光功率过低"
            oms_source_sub_name = None
            oms_target_sub_name = None
            sys_name = None
            source_ne_name = ""
            district_county = ""
            manufactor = ""
            input_find = next(filter(lambda find: find['ne_id'] == source_ne_id, input_Optical_Nes), None)
            if input_find:
                district_county = input_find['district_county']
                manufactor = input_find['manufactor']
            
            calc_find = next(filter(lambda find: find['source_ne_id'] == source_ne_id or find['target_ne_id'] == source_ne_id, calc_Ne_Adjs), None)
            if calc_find:
                sys_name = calc_find['sys_name']
            source = next(filter(lambda find: find['source_ne_id'] == source_ne_id, calc_ne_oas), None)
            if source:
                source_ne_name = source['source_oa_sub_name']
            calc_Ola_find = next(filter(lambda find: find['ola_ne_id'] == source_ne_id, calc_Ola_Business_Waves), None)
            if calc_Ola_find:
                oms_source_sub_name = calc_Ola_find['oms_source_sub_name']
                oms_target_sub_name = calc_Ola_find['oms_target_sub_name']
            else:
                calc_Otm_find = next(filter(lambda find: (find['source_ne_id'] == item['source_ne_id'] and find['source_oa_shelf_id'] == item['source_oa_shelf_id'] and find['source_oa_slot_id'] == item['source_oa_slot_id']) or \
                    (find['target_ne_id'] == item['source_ne_id'] and find['target_oa_shelf_id'] == item['source_oa_shelf_id'] and find['target_oa_slot_id'] == item['source_oa_slot_id']), calc_Otm_Business_Waves), None)
                if calc_Otm_find:
                    oms_source_sub_name = calc_Otm_find['oms_source_sub_name']
                    oms_target_sub_name = calc_Otm_find['oms_target_sub_name']
            if not source_ne_name and not sys_name:
                return
            risk_hash = Md5Generator.md5(source_ne_id + "--" + source_shelf_id + "--" + source_slot_id + "--" + risk_type)
            old_order = next(filter(lambda find: find['risk_hash'] == risk_hash and find['is_top_end'] != 1, old_order_list), None)
            if old_order:
                return
            order_Lists.append({
                "risk_id": str(uuid.uuid4()),
                "risk_hash": risk_hash,
                "source_ne_id": source_ne_id,
                "source_ne_sub_name": source_ne_name,
                "source_shelf_id": source_shelf_id,
                "source_slot_id": source_slot_id,
                "target_ne_id": "",
                "target_ne_sub_name": "",
                "city": item['city'],
                "district_county": district_county,
                "sys_name": sys_name,
                "oms": oms_source_sub_name + self.slash + oms_target_sub_name,
                "network_level": item['net_level'],
                "manufactor": manufactor,
                "risk_level": risk_level,
                "risk_type": risk_type,
                "risk_content": source_ne_name + self.slash + item['source_oa_shelf_id'] + self.slash + item['source_oa_slot_id'] + self.slash + risk_type,
                "current_value": item['oa_output_power_std_dev_risk'],
                "standard_value": item['standard_wave_output'],
                "unit_measurement": "dBm",
                "discover_time": item['timestamp'],
                "is_send_top": 0,
                "is_top_end": 0,
                "timestamp": item['timestamp'],
                "is_history": 2
            })
        OrderList.bulk_add(order_Lists)
            
    def ComputedFront_picture_otm(self):
        front_Picture_Otms = []
        business_s = getFront_picture_otmCom()
        calc_Oms = CalcOms.get(is_history=2)
        risk_Olps = RiskOlp.get_all_except({"is_risk": 'ok'}, is_history=2)
        for item in business_s:
            directions = 0
            is_olp = 0
            ne_type = item['ne_type']
            directions = len(list(
                filter(lambda find: find['oms_source_id'] == item['source_ne_id'] or \
                    find['oms_target_id'] == item['source_ne_id'], calc_Oms)))
            if not ne_type.find(self.siteROADM):
                is_olp = 1 if next(filter(lambda find: find['olp_ne_id'] == item['source_ne_id'], risk_Olps), None) else 0
            front_Picture_Otms.append({
                "source_ne_id": item['source_ne_id'],
                "ne_type": item['ne_type'],
                "directions": directions,
                "is_olp": is_olp,
                "picture_id": item['ne_type'] + self.slash + directions + self.slash + is_olp,
                "direction_1": "",
                "direction_2": "",
                "direction_3": "",
                "direction_4": "",
                "direction_5": "",
                "direction_6": "",
                "direction_7": "",
                "direction_8": "",
                "direction_1_in_oa_fingerprint": "",
                "direction_2_in_oa_fingerprint": "",
                "direction_3_in_oa_fingerprint": "",
                "direction_4_in_oa_fingerprint": "",
                "direction_5_in_oa_fingerprint": "",
                "direction_6_in_oa_fingerprint": "",
                "direction_7_in_oa_fingerprint": "",
                "direction_8_in_oa_fingerprint": "",
                "direction_1_out_oa_fingerprint": "",
                "direction_2_out_oa_fingerprint": "",
                "direction_3_out_oa_fingerprint": "",
                "direction_4_out_oa_fingerprint": "",
                "direction_5_out_oa_fingerprint": "",
                "direction_6_out_oa_fingerprint": "",
                "direction_7_out_oa_fingerprint": "",
                "direction_8_out_oa_fingerprint": "",
                "timestamp": item['timestamp'],
                "is_history": 2
            })
        FrontPictureOtm.bulk_add(front_Picture_Otms)

    def ComputedFront_picture_ola(self):
        _Ne_Oas = CalcNeOas.get(is_history=2)
        front_Picture_OlaComs = getFront_picture_olaCom()
        front_Picture_Olas = []
        for item in front_Picture_OlaComs:
            out_oa_shelf_id = ""
            out_oa_slot_id = ""
            calc_Ne = next(
                filter(lambda find: find['source_ne_id'] == item['source_ne_id'] and \
                    find['source_oa_in_out_id'] == self.send and \
                        find['target_oa_sub_name'] != item['target_oa_sub_name'], _Ne_Oas), None)
            if calc_Ne:
                out_oa_shelf_id = calc_Ne['source_oa_shelf_id']
                out_oa_slot_id = calc_Ne['source_oa_slot_id']
            front_Picture_Olas.append({
                "source_ne_id": item['source_ne_id'],
                "source_oa_sub_name": item['source_oa_sub_name'],
                "in_target_ne_id": item['target_ne_id'],
                "in_target_ne_name": item['target_oa_sub_name'],
                "in_oa_shelf_id": item['source_oa_shelf_id'],
                "in_oa_slot_id": item['source_oa_slot_id'],
                "out_oa_shelf_id": out_oa_shelf_id,
                "out_oa_slot_id": out_oa_slot_id,
                "oa_num": 2 if ((item['source_oa_shelf_id'] + self.slash + item['source_oa_slot_id']) != (out_oa_shelf_id + self.slash + out_oa_slot_id)) else 1,
                "timestamp": item['timestamp'],
                "is_history": 2
            })
        FrontPictureOla.bulk_add(front_Picture_Olas)
        
    def ComputedFront_data_oa(self):
        dataRikoa = RiskOa.get(is_history=2)
        _Stands = TopOaStand.get(is_history=2)
        _InputPmData = InputPmData.get(is_history=2)
        _ClacOaStand = CalcOaStand.get(is_history=2)
        _InputOaBoardType = InputOaBoardType.get_input_oa_board_types(is_history=2)
        _Calc_otm_business_waves = CalcOtmBusinessWaves.get(is_history=2)
        _Calc_ola_Business_waves = CalcOlaBusinessWaves.get(is_history=2)
        calc_Incoming = CalcIncomingOpticalPower.get(is_history=2)
        input_Internal_s = InputInternalTopology.get(is_history=2)
        _Ne_Oas = CalcNeOas.get(is_history=2)
        input_Voa_Configs = InputVoaConfig.get_input_voa_configs(is_history=2)
        front_Data_Oa_Coms = []
        front_Data_Oas = []
        
        for item in dataRikoa:
            source_ne_id = item['source_ne_id']
            source_oa_shelf_id = item['source_oa_shelf_id']
            source_oa_slot_id = item['source_oa_slot_id']
            board_model = ""
            oms_otm = "null"
            oms_ola = "null"
            wavs_otm = -1
            wavs_ola = -1
            out_power = 0
            in_power = 0
            standard_wave_output = 0
            standard_gain_min = 0
            standard_gain_max = 0
            incoming_optical_power = 0
            
            input_Pm_Data_find = next(
                filter(lambda find: find['a_ne_id'] == source_ne_id and find['shelf_id'] == source_oa_shelf_id and \
                    find['slot_id'] == source_oa_slot_id, _InputPmData), None)
            calc_Oa_Stand_find = next(
                filter(lambda find: find['oa_fingerprint'] == (source_ne_id + self.slash + source_oa_shelf_id + self.slash + source_oa_slot_id), _ClacOaStand), None)
            input_Oa_Board_Type_find = next(filter(lambda find: find['ne_id'] == source_ne_id and find['shelf_id'] == source_oa_shelf_id and \
                find['slot_id'] == source_oa_slot_id, _InputOaBoardType), None)
            calc_Otm_Business_Waves_find = next(filter(lambda find: find['source_ne_id'] == source_ne_id and find['source_oa_shelf_id'] == source_oa_shelf_id and \
                find['source_oa_slot_id'] == source_oa_slot_id, _Calc_otm_business_waves), None)
            calc_Incoming_Optical_Power_find = next(filter(lambda find: find['oa_fingerprint'] == (source_ne_id + self.slash + source_oa_shelf_id + self.slash + source_oa_slot_id), calc_Incoming), None)
            if input_Pm_Data_find:
                out_power = input_Pm_Data_find['out_power']
                in_power = input_Pm_Data_find['in_power']
            if calc_Oa_Stand_find:
                standard_wave_output = calc_Oa_Stand_find['standard_wave_output']
                standard_gain_min = calc_Oa_Stand_find['standard_gain_min']
                standard_gain_max = calc_Oa_Stand_find['standard_gain_max']
            if input_Oa_Board_Type_find:
                board_model = input_Oa_Board_Type_find['board_model']
            if calc_Otm_Business_Waves_find:
                wavs_otm = calc_Otm_Business_Waves_find['business_waves']
                oms_otm = calc_Otm_Business_Waves_find['oms_source_sub_name'] + "-" + calc_Otm_Business_Waves_find['oms_target_sub_name']
            else:
                calc_Ola_Business_Waves_find = next(filter(lambda find: find['ola_ne_id'] == source_ne_id, _Calc_ola_Business_waves), None)
                if calc_Ola_Business_Waves_find:
                    wavs_ola = calc_Ola_Business_Waves_find['business_waves']
                    oms_ola = calc_Ola_Business_Waves_find['oms_source_sub_name'] + "-" + calc_Ola_Business_Waves_find['oms_target_sub_name']
            if calc_Incoming_Optical_Power_find:
                incoming_optical_power = calc_Incoming_Optical_Power_find['incoming_optical_power']
            
            front_Data_Oa_Coms.append({
                "source_ne_id": source_ne_id,
                "source_oa_shelf_id": source_oa_shelf_id,
                "source_oa_slot_id": source_oa_slot_id,
                "out_power": out_power,
                "in_power": in_power,
                "standard_wave_output": standard_wave_output,
                "standard_gain_min": standard_gain_min,
                "standard_gain_max": standard_gain_max,
                "board_model": board_model,
                "wavs_otm": wavs_otm,
                "oms_otm": oms_otm,
                "wavs_ola": wavs_ola,
                "oms_ola": oms_ola,
                "sum_risks": item['sum_risks'],
                "incoming_optical_power": incoming_optical_power,
                "timestamp": item['timestamp']
            })
        for item in front_Data_Oa_Coms:
            gain = item['out_power'] - item['in_power']
            inside_voa = 0
            outside_voa = 0
            output_stand_power = 0
            in_ne_subname = ""
            out_ne_subname = ""
            oms = item['oms_ola'] if item['oms_otm'] == "null" else item['oms_otm']
            wavs = item['wavs_ola'] if item['wavs_otm'] == -1 else item['wavs_otm']
            calc_Incoming_ = next(
                filter(lambda find: find['oa_fingerprint'] == (item['source_ne_id'] + self.slash + item['source_oa_shelf_id'] + self.slash + item['source_oa_slot_id']), calc_Incoming), None)
            if calc_Incoming_:
                inside_voa = calc_Incoming_['internal_voa']
                outside_voa = calc_Incoming_['outside_voa']
            oa_Stand = next(filter(lambda find: find['oa_fingerprint'] == (item['source_ne_id'] + self.slash + item.source_oa_shelf_id + self.slash + item['source_oa_slot_id']), _Stands), None)
            if oa_Stand:
                output_stand_power = oa_Stand['manual_standard_wave_output']
            else:
                output_stand_power = item['standard_wave_output']
            calc_put = next(filter(lambda find: find['source_ne_id'] == item['source_ne_id'] and \
                find['source_oa_shelf_id'] == item['source_oa_shelf_id'] and find['source_oa_slot_id'] == item['source_oa_slot_id'] and find['source_oa_in_out_id'] == self.put, _Ne_Oas), None)
            calc_send = next(filter(lambda find: find['source_ne_id'] == item['source_ne_id'] and \
                find['source_oa_shelf_id'] == item['source_oa_shelf_id'] and find['source_oa_slot_id'] == item['source_oa_slot_id'] and find['source_oa_in_out_id'] == self.send, _Ne_Oas), None)
            if calc_put:
                in_ne_subname = calc_put['target_oa_sub_name']
            if calc_send:
                out_ne_subname = calc_send['target_oa_sub_name']
            front_Data_Oas.append({
                "ne_id": item['source_ne_id'],
                "shelf_id": item['source_oa_shelf_id'],
                "slot_id": item['source_oa_slot_id'],
                "outside_voa": outside_voa,
                "inside_voa": inside_voa,
                "input_power": item['in_power'],
                "input_stand_power": output_stand_power - gain,
                "output_power": item['out_power'],
                "output_stand_power": output_stand_power,
                "gain": gain,
                "stand_gain_min": item['standard_gain_min'],
                "stand_gain_max": item['standard_gain_max'],
                "brd_type": item['board_model'],
                "wavs": wavs,
                "oms": oms,
                "oa_risk_num": item['sum_risks'],
                "in_ne_subname": in_ne_subname,
                "out_ne_subname": out_ne_subname,
                "ne_incoming_power": item['incoming_optical_power'],
                "ne_outing_power": 0,
                "timestamp": item['timestamp'],
                "is_history": 2
            })
        FrontDataOa.bulk_add(front_Data_Oas)

    def ComputedFront_data_fiber(self):
        calc_Adj = CalcNeAdj.get(is_history=2)
        calc_Oas = CalcNeOas.get(is_history=2)
        input_Pm_Datas = InputPmData.get(is_history=2)
        risk_Fibers = RiskFiber.get(is_history=2)
        calc_Incoming = CalcIncomingOpticalPower.get(is_history=2)
        _Data_Fibers = []
        calc_Oa_Powers = CalcOaPower.get(is_history=2)
        for item in calc_Adj:
            source_out_fiber_loss = 0
            source_in_fiber_loss = 0
            source_outing_power = 0
            source_incoming_power = 0
            target_outing_power = 0
            target_incoming_power = 0
            source_out_shelf_slot = ""
            target_in_shelf_slot = ""
            source_in_shelf_slot = ""
            target_out_shelf_slot = ""
            is_risk = ""
            
            source_oas = next(filter(lambda find: find['source_ne_id'] == item['source_ne_id'] and find['target_ne_id'] == item['target_ne_id'] and \
                find['act_stand'] == item['act_stand'] and find['source_oa_in_out_id'] == self.send, calc_Oas), None)
            target_oas = next(filter(lambda find: find['source_ne_id'] == item['source_ne_id'] and find['target_ne_id'] == item['target_ne_id'] and \
                find['act_stand'] == item['act_stand'] and find['source_oa_in_out_id'] == self.put, calc_Oas), None)
            if source_oas:
                source_out_fiber_loss = source_oas['fiber_loss']
                source_oa_fingerprint = source_oas['source_oa_fingerprint'].split(self.slash)
                target_oa_fingerprint = source_oas['target_oa_fingerprint'].split(self.slash)
                source_out_shelf_slot = source_oa_fingerprint[1] + self.slash + source_oa_fingerprint[2]
                target_in_shelf_slot = target_oa_fingerprint[1] + self.slash + target_oa_fingerprint[2]
                
                oa_Power_source_outing = next(
                    filter(lambda find: find['source_ne_id'] == source_oa_fingerprint[0] and find['source_oa_shelf_id'] == source_oa_fingerprint[1] and \
                        find['source_oa_slot_id'] == source_oa_fingerprint[2], calc_Oa_Powers), None)
                if oa_Power_source_outing:
                    source_outing_power = oa_Power_source_outing['outing_power']
                oa_Power_source_incoming = next(filter(lambda find: find['source_ne_id'] == target_oa_fingerprint[0] and find['source_oa_shelf_id'] == target_oa_fingerprint[1] and \
                    find['source_oa_slot_id'] == target_oa_fingerprint[2], calc_Oa_Powers), None)
                if oa_Power_source_incoming:
                    target_incoming_power = oa_Power_source_incoming['incoming_power']
            
            if target_oas:
                source_in_fiber_loss = target_oas['fiber_loss']
                source_oa_fingerprint = target_oas['source_oa_fingerprint'].split(self.slash)
                target_oa_fingerprint = target_oas['target_oa_fingerprint'].split(self.slash)
                source_in_shelf_slot = source_oa_fingerprint[1] + self.slash + source_oa_fingerprint[2]
                target_out_shelf_slot = target_oa_fingerprint[1] + self.slash + target_oa_fingerprint[2]
                oa_Power_target_outing = next(filter(lambda find: find['source_ne_id'] == target_oa_fingerprint[0] and find['source_oa_shelf_id'] == target_oa_fingerprint[1] and \
                    find['source_oa_slot_id'] == target_oa_fingerprint[2], calc_Oa_Powers), None)
                if oa_Power_target_outing:
                    target_outing_power = oa_Power_target_outing['outing_power']
                oa_Power_target_incoming = next(filter(lambda find: find['source_ne_id'] == source_oa_fingerprint[0] and find['source_oa_shelf_id'] == source_oa_fingerprint[1] and \
                    find['source_oa_slot_id'] == source_oa_fingerprint[2], calc_Oa_Powers), None)
                if oa_Power_target_incoming:
                    source_incoming_power = oa_Power_target_incoming['incoming_power']
            
            risk_IsRisk = next(filter(lambda find: (find['source_ne_id'] == item['source_ne_id'] and find['target_ne_id'] == item['target_ne_id']) or \
                (find['source_ne_id'] == item['target_ne_id'] and find['target_ne_id'] == item['source_ne_id']) and find['act_stand'] == item['act_stand'], risk_Fibers), None)
            if risk_IsRisk:
                is_risk = risk_IsRisk['is_risk']
            _Data_Fibers.append({
                "source_ne_id": item['source_ne_id'],
                "target_ne_id": item['target_ne_id'],
                "act_stand": item['act_stand'],
                "source_sub_name": item['source_sub_name'],
                "target_sub_name": item['target_sub_name'],
                "fiber_name": item['fiber_name'],
                "fiber_length": item['fiber_length'],
                "stand_fiber_loss": item['stand_fiber_loss'],
                "source_out_fiber_loss": source_out_fiber_loss,
                "source_in_fiber_loss": source_in_fiber_loss,
                "source_outing_power": source_outing_power,
                "source_incoming_power": source_incoming_power,
                "source_out_shelf_slot": source_out_shelf_slot,
                "source_in_shelf_slot": source_in_shelf_slot,
                "target_outing_power": target_outing_power,
                "target_incoming_power": target_incoming_power,
                "target_out_shelf_slot": target_out_shelf_slot,
                "target_in_shelf_slot": target_in_shelf_slot,
                "is_risk": is_risk,
                "timestamp": item['timestamp'],
                "is_history": 2
            })
        FrontDataFiber.bulk_add(_Data_Fibers)
    
    def ComputedFront_city_Permission(self):
        input_topology_data_list = InputTopologyData.distincet_get(is_history=2)
        front_city_permission_list = []
        for item in input_topology_data_list:
            front_city_permission_list.append({
                "sys_name": item['sys_name'],
                "city": item['city'],
                "net_level": item['net_level'],
                "is_history": 2
            })
        FrontCityPermission.bulk_add(input_topology_data_list)

    def ComputedFront_ne(self):
        calc_Ne_Oas = CalcNeOas.get(is_history=2)
        input_Optical = InputOpticalNe.get(is_history=2)
        input_Topologies = InputTopologyData.get(is_history=2)
        risk_Oas = RiskOa.get(is_history=2)
        front_Nes = []
        for item in calc_Ne_Oas:
            oa_color = 0
            sys_name = ""
            manufactor = ""
            ne_type = ""
            ne_model = ""
            optical_ne_find = next(filter(lambda find: find['ne_id'] == item['source_ne_id'], input_Optical), None)
            if optical_ne_find:
                manufactor = optical_ne_find['manufactor']
                ne_type = optical_ne_find['ne_type']
                ne_model = optical_ne_find['ne_model']
            topology_data_find = next(
                filter(lambda find: (find['a_oa_fingerprint'] == item['source_oa_fingerprint'] and find['z_oa_fingerprint'] == item['target_oa_fingerprint']) or \
                    (find['a_oa_fingerprint'] == item['target_oa_fingerprint'] and find['z_oa_fingerprint'] == item['source_oa_fingerprint']), input_Topologies), None)
            if topology_data_find:
                sys_name = topology_data_find['sys_name']
            risk_find = next(filter(lambda find: find['source_ne_id'] == item['source_ne_id'] and find['source_oa_shelf_id'] == item['source_oa_shelf_id'] and \
                find['source_oa_slot_id'] == item['source_oa_slot_id'], risk_Oas), None)
            if risk_find:
                if risk_find['is_input_power_fluc_emergency'] == self.er_ok and risk_find['is_output_power_fluc_emergency'] == self.er_ok and \
                    risk_find['is_output_power_dev_emergency'] == self.er_ok:
                    if risk_find['is_input_power_fluc_risk'] == self.ok and risk_find['is_output_power_fluc_risk'] == self.ok and \
                        risk_find['is_gain_risk'] == self.ok and risk_find['is_output_power_dev_risk'] == self.ok:
                        oa_color = 0
                    else:
                        oa_color = 1
                else:
                    oa_color = 2
            
            front_Nes.append({
                "sys_name": sys_name,
                "source_ne_id": item['source_ne_id'],
                "source_oa_sub_name": item['source_oa_sub_name'],
                "source_oa_shelf_id": item['source_oa_shelf_id'],
                "source_oa_slot_id": item['source_oa_slot_id'],
                "source_oa_fingerprint": item['source_oa_fingerprint'],
                "source_oa_in_out_id": item['source_oa_in_out_id'],
                "target_ne_id": item['target_ne_id'],
                "target_oa_sub_name": item['target_oa_sub_name'],
                "target_oa_slot_id": item['target_oa_slot_id'],
                "target_oa_shelf_id": item['target_oa_shelf_id'],
                "target_oa_fingerprint": item['target_oa_fingerprint'],
                "target_oa_in_out_id": item['target_oa_in_out_id'],
                "act_stand": item['act_stand'],
                "manufactor": manufactor,
                "ne_type": ne_type,
                "ne_model": ne_model,
                "oa_color": oa_color,
                "timestamp": item['timestamp'],
                "is_history": 2
            })
        FrontNe.bulk_add(front_Nes)
           
    def ComputedFront_adj(self):
        calc_Ne_Adjs = CalcNeAdj.get(is_history=2)
        front_Nes = FrontNe.get(is_history=2)
        risk_Fibers = RiskFiber.get(is_history=2)
        risk_Oas = RiskOa.get(is_history=2)
        front_Adjs = []
        
        for item in calc_Ne_Adjs:
            source_ne_id = item['source_ne_id']
            target_ne_id = item['target_ne_id']
            sys_name = item['sys_name']
            acr_stand = item['act_stand']
            source_ne_color = self.Computed_ne_color(front_Nes, risk_Oas, sys_name, source_ne_id)
            target_ne_color = self.Computed_ne_color(front_Nes, risk_Oas, sys_name, target_ne_id)
            fiber_color = self.Computed_fiber_color(risk_Fibers, source_ne_id, target_ne_id, acr_stand)
            
            front_Adjs.append({
                "source_ne_id": source_ne_id,
                "source_sub_name": item['source_sub_name'],
                "source_ne_type": item['source_ne_type'],
                "target_ne_id": target_ne_id,
                "target_sub_name": item['target_sub_name'],
                "target_ne_type": item['target_ne_type'],
                "sys_name": sys_name,
                "act_stand": item['act_stand'],
                "fiber_length": item['fiber_length'],
                "source_ne_color": source_ne_color,
                "target_ne_color": target_ne_color,
                "fiber_color": fiber_color,
                "timestamp": item['timestamp'],
                "is_history": 2
            })
        FrontAdj.bulk_add(front_Adjs)
        
    def ComputedSystem_label(self):
        order_Lists = OrderList.get_orders(is_history=2)
        _LabelComs = getSystem_label_Com()
        system_Labels = []
        system_labelGroup = groupby(_LabelComs, key=lambda x: x['sys_name'])
        for item in system_labelGroup:
            risk_sum = 0
            sys_atc_fiber_length = 0
            sys_standby_fiber_length = 0
            first = item[0] if item and len(item) > 0 else None
            if first is None or first['sys_name'] == "":
                continue
            if len(item) > 1:
                last = item[-1]
                for act in item:
                    if act['act_stand'] == "主":
                        sys_atc_fiber_length = act['sum_fibers_length']
                    elif act['act_stand'] == "备":
                        sys_standby_fiber_length = act['sum_fibers_length']
            else:
                sys_atc_fiber_length = first['sum_fibers_length']
            
            orders_risk_sum = list(filter(lambda find: find['sys_name'] == first['sys_name'] and (find['top_order_end_time'] == "" or find['top_order_end_time'] is None, order_Lists)))
            if orders_risk_sum:
                risk_sum = len(orders_risk_sum)
            system_Labels.append({
                "system_name": first['sys_name'],
                "full_waves": first['full_waves'],
                "sys_atc_fiber_length": sys_atc_fiber_length,
                "sys_standby_fiber_length": sys_standby_fiber_length,
                "risk_sum": risk_sum,
                "timestamp": first['timestamp'],
                "is_history": 2
            })
        SystemLabel.bulk_add(system_Labels)
        
    def RemoveIshistoryOne(self):
        MysqltableOperation(SqlOperation.UPDATE.value, 1, 11)
    
    def UpdateIshistoryZero_One(self):
        MysqltableOperation(SqlOperation.UPDATE.value, 0, 1)

    def UpdateIshistoryTwo_Zero(self):
        MysqltableOperation(SqlOperation.UPDATE.value, 2, 0)

    def rollback(self):
        deleteDataState("input_oms_business_waves", [0, 13])
        deleteDataState("input_threshold", [0, 13])
        removeDataState("input_oms_business_waves", 12, 0)
        removeDataState("input_threshold", 12, 0)

    def sendSingle(self):
        pass    
    
    def setComputing_mode(self, state):
        obj = ComputingMode.get_all_computing_mode()
        if len(obj) == 0:
            ComputingMode.add(sys_name="DEFAULT", state=state,
                            timestamp=datetime.now(),
                            is_history=0)
        else:
            for item in obj:
                item.update({'id': item[id]}, state=state)

    
def reStartComputed():
    prepare()
    CopyData()
    public_fuc()
    

def start_computed():
    prepare()
    computer.set_mysql_database()
    public_fuc()
