from sqlalchemy import text
from ..models.order_list import OrderList
import datetime
from common.database import Tr_Session
from dateutil.relativedelta import relativedelta


def join_arr(param):
    search = "("
    for item in param:
        if item == "二干/省内骨干网":
            continue
        search += f"'{item}',"
    
    if len(search) > 1:
        search = search[:-1] + ")"
    else:
        search += "')"
    
    return search


def check_search(data, prefix=""):
    where = "where"
    and_ = "and"
    search_cmd = ""
    if prefix == "":
        search_cmd = where
    else:
        search_cmd = prefix + " " + and_
    if data.city and "all" not in data.city:
        search_cmd += " city = '" + data.city + "' " + and_
    if data.network_level and "all" not in data.network_level:
        search_cmd += " network_level = '" + data.network_level + "' " + and_
    if data.startTime and data.endTime:
        search_cmd += " discover_time between '" + data.startTime + "' and '" + data.endTime + "'"
    where_index = search_cmd.rfind(where)
    and_index = search_cmd.rfind(and_)
    length = len(search_cmd)
    if (length - where_index) == len(where):
        search_cmd = ""
    elif (length - and_index) == len(and_):
        search_cmd = search_cmd[:and_index]
    return search_cmd


class OrderListService(object):

    def __init__(self, startTime, endTime, city, network_level):
        self.startTime = startTime
        self.endTime = endTime
        self.city = city
        self.network_level = network_level
        self.val = 0
        self.statistic = {}
        self.network_levels = {}
        self.citys = {}
        self.annual_statistics = {}
        self.city_statistics = {}
        self.last_year_date = datetime.date.today() + relativedelta(months=-11)

    def __load_from_db(self):
        start_time = self.startTime
        end_time = self.endTime
        city = self.city
        network_level = self.network_level
        kwargs = {}
        self.annual_statistics.clear()

        if city and len(city) > 0:
            kwargs['city'] = city
        if network_level != 'all':
            kwargs['network_level'] = network_level
            
        print(f"start_time: {str(start_time)}")
        print(f"end_time: {str(end_time)}")
        # if len(start_time) > 0 and len(end_time) > 0:
        if start_time and end_time:
            self.data = OrderList.get_orders_by_time(start_time, end_time, **kwargs)
        else:
            self.data = OrderList.get_orders(**kwargs)

    def get_handled_data(self, cmd_list, deal_all=False):
        self.__load_from_db()
        self.__init_annual_statistics()
        for it in self.data:
            # 设置 unhandled 信息
            self.val = self.val + 1
            # 设置统计信息
            if 'statistics' in cmd_list or deal_all:
                self.__set_statistic(it)
            # 设置network_level 信息
            if 'network_level' in cmd_list or deal_all:
                self.__set_network_level(it)
            # 设置city统计信息
            if 'city_group' in cmd_list or deal_all:
                self.__set__city_group(it)
            # 设置 年统计信息
            if 'annual_statistics' in cmd_list or deal_all:
                self.__set_annual_statistics(it)
            # 设置 city risk_level 统计信息
            if 'city_statistics' in cmd_list or deal_all:
                self.__set_city_statistics(it)

    def __init_annual_statistics(self):
        today = datetime.date.today()
        begin_date = today + relativedelta(months=-11)
        if len(self.annual_statistics) == 0:
            while begin_date <= today:
                self.annual_statistics[begin_date.month] = {
                    'count': 0,
                    'untreatedCount': 0,
                    'processedCount': 0
                }
                begin_date += relativedelta(months=1)

    def __set_statistic(self, it):
        if self.statistic.get(it.risk_type) is None:
            self.statistic[it.risk_type] = 1
        else:
            self.statistic[it.risk_type] += 1

    def __set_network_level(self, it):
        level_name = it.network_level if len(it.network_level) > 0 else "(null)"

        if self.network_levels.get(level_name) is None:
            self.network_levels[level_name] = 1
        else:
            self.network_levels[level_name] += 1

    def __set__city_group(self, it):

        if self.citys.get(it.city) is None:
            self.citys[it.city] = {
                'untreatedCount': 1 if it.is_top_end == 0 else 0,
                'processedCount': 0 if it.is_top_end == 0 else 1,
                'count': 1
            }
        else:
            self.citys[it.city]['count'] += 1
            if it.is_top_end == 0:
                self.citys[it.city]['untreatedCount'] += 1
            else:
                self.citys[it.city]['processedCount'] += 1

    def __set_annual_statistics(self, it):
        if it.timestamp.date() >= self.last_year_date:
            self.annual_statistics[it.timestamp.month]['count'] += 1
            if it.is_top_end == 1:
                self.annual_statistics[it.timestamp.month]['processedCount'] += 1
            else:
                self.annual_statistics[it.timestamp.month]['untreatedCount'] += 1

    def __set_city_statistics(self, it):
        if self.city_statistics.get(it.city) is None:
            self.city_statistics[it.city] = {
                'general_count': 0,
                'general_untreatedCount': 0,
                'general_processedCount': 0,
                'emergency_count': 0,
                'emergency_untreatedCount': 0,
                'emergency_processedCount': 0
            }
            if it.risk_level == '一般':
                self.city_statistics[it.city]['general_count'] += 1
                if it.is_top_end == 1:
                    self.city_statistics[it.city]['general_processedCount'] += 1
                else:
                    self.city_statistics[it.city]['general_untreatedCount'] += 1
            elif it.risk_level == '紧急':
                self.city_statistics[it.city]['emergency_count'] += 1
                if it.is_top_end == 1:
                    self.city_statistics[it.city]['emergency_processedCount'] += 1
                else:
                    self.city_statistics[it.city]['emergency_untreatedCount'] += 1
        else:
            if it.risk_level == '一般':
                self.city_statistics[it.city]['general_count'] += 1
                if it.is_top_end == 1:
                    self.city_statistics[it.city]['general_processedCount'] += 1
                else:
                    self.city_statistics[it.city]['general_untreatedCount'] += 1
            elif it.risk_level == '紧急':
                self.city_statistics[it.city]['emergency_count'] += 1
                if it.is_top_end == 1:
                    self.city_statistics[it.city]['emergency_processedCount'] += 1
                else:
                    self.city_statistics[it.city]['emergency_untreatedCount'] += 1

    def get_unhandled(self):
        return {
            'max': self.val,
            'val': self.val
        }

    def get_statistics(self):
        return [{'name': key, 'content': key, 'count': val, 'value': val}
                for key, val in self.statistic.items()]

    def get_network_level(self):
        return [{'name': key, 'content': key, 'count': val, 'value': val}
                for key, val in self.network_levels.items()]

    def get_hidden_network_level(self):
        rtn_list = []
        for key, val in self.network_levels.items():
            if key != '(null)':
                rtn_list.append(
                    {
                        'name': key,
                        'value': val
                    }
                )
        return rtn_list

    def get_city_statistics(self):
        return [{'id': '',
                 'city': key,
                 'count': val['count'],
                 'untreatedCount': val['untreatedCount'],
                 'processedCount': val['processedCount']} for key, val in self.citys.items()]

    def get_annual_statistics(self):
        return [{
                 'timestamp': '%02d' % key,
                 'count': val['count'],
                 'untreatedCount': val['untreatedCount'],
                 'processedCount': val['processedCount']}
                for key, val in self.annual_statistics.items()]

    def get_city_risk_level_statistics(self):
        return [{
            'city': key,
            'general_count': val['general_count'],
            'general_untreatedCount': val['general_untreatedCount'],
            'general_processedCount': val['general_processedCount'],
            'emergency_count': val['emergency_count'],
            'emergency_untreatedCount': val['emergency_untreatedCount'],
            'emergency_processedCount': val['emergency_processedCount']}
            for key, val in self.city_statistics.items()]

    @classmethod
    def get_filter_data(cls, **kwargs):
        return [{
            'city': item[0],
            'district_county': item[1],
            'sys_name': item[2],
            'network_level': item[3],
            'risk_level': item[4]
        } for item in OrderList.get_filter(**kwargs)]

    @classmethod
    def get_trouble_by_filter(cls, **kwargs):
        total, items = OrderList.get_trouble_by_filter(**kwargs)
        return total, ({
            'id': item.id,
            'order_id': item.order_id,
            'discover_time': item.discover_time,
            'city': item.city,
            'district_county': item.district_county,
            'sys_name': item.sys_name,
            'oms': item.oms,
            'network_level': item.network_level,
            'manufactor': item.manufactor,
            'risk_level': item.risk_level,
            'risk_content': item.risk_content,
            } for item in items)
        
        # return total, [{
        #     'id': item.id,
        #     'order_id': item.order_id,
        #     'risk_id': item.risk_id,
        #     'risk_hash': item.risk_hash,
        #     'source_ne_id': item.source_ne_id,
        #     'source_ne_sub_name': item.source_ne_sub_name,
        #     'source_shelf_id': item.source_shelf_id,
        #     'source_slot_id': item.source_slot_id,
        #     'target_ne_id': item.target_ne_id,
        #     'target_ne_sub_name': item.target_ne_sub_name,
        #     'city': item.city,
        #     'district_county': item.district_county,
        #     'sys_name': item.sys_name,
        #     'oms': item.oms,
        #     'network_level': item.network_level,
        #     'manufactor': item.manufactor,
        #     'risk_level': item.risk_level,
        #     'risk_type': item.risk_type,
        #     'risk_content': item.risk_content,
        #     'current_value': item.current_value,
        #     'standard_value': item.standard_value,
        #     'unit_measurement': item.unit_measurement,
        #     'discover_time': item.discover_time,
        #     'is_send_top': item.is_send_top,
        #     'is_top_end': item.is_top_end,
        #     'top_feedback_message': item.top_feedback_message,
        #     'top_order_end_time': item.top_order_end_time,
        #     'timestamp': item.timestamp,
        #     'is_history': item.is_history
        #     } for item in items]

    @classmethod
    def getTop_end(cls, req):
        with Tr_Session() as session:
            cmd = "select (select count(*) from `order_list` " + check_search(req) + ") tabCount,count(*) top_endCount from `order_list`" + check_search(req, " where is_top_end = '0' ") + ";"
            return session.execute(text(cmd))

    @classmethod
    def getRisk_typeGroup(cls, req):
        with Tr_Session() as session:
            cmd = "select count(*) count,risk_type from `order_list` " + check_search(req) + " group by risk_type;"
            return session.execute(text(cmd))

    @classmethod
    def getNetwork_levelGroup(cls, req):
        with Tr_Session() as session:
            cmd = "select count(*) count,network_level from order_list " + check_search(req) + " group by network_level;"
            return session.execute(text(cmd))

    @classmethod
    def getHiddenCityGroup(cls):
        with Tr_Session() as session:
            cmd = """select orders.*,coalesce(untreated.count,0) untreatedCount,coalesce(processed.count,0) processedCount from 
            (select city,count(*) count from order_list group by city) 
            orders left join (select city,count(*) count from order_list where is_top_end = 0 group by city) untreated 
            on orders.city = untreated.city 
            left join (select city,count(*) count from order_list where is_top_end = 1 group by city) processed 
            on orders.city = processed.city order by untreatedCount desc;"""
            return session.execute(text(cmd))
    
    @classmethod
    def getAnnualRiskGroup(cls):
        with Tr_Session() as session:
            cmd = """select orders.*,coalesce(untreated.count,0) untreatedCount,coalesce(processed.count,0) processedCount from (select count(is_top_end) count,date_format(timestamp,'%m') timestamp from order_list group by date_format(timestamp,'%m')) orders 
            left join(select date_format(timestamp,'%m') timestamp,count(is_top_end) count from order_list where is_top_end = 0 group by date_format(timestamp, '%m')) untreated 
            on orders.timestamp = untreated.timestamp 
            left join(select date_format(timestamp,'%m') timestamp,count(is_top_end) count from order_list where is_top_end = 1 group by date_format(timestamp, '%m')) processed 
            on orders.timestamp = processed.timestamp;"""
            return session.execute(text(cmd))

    @classmethod
    def getHiddenNetwork(cls):
        with Tr_Session() as session:
            cmd = "select distinct network_level from `order_list` where network_level != '' group by network_level;"
            return session.execute(text(cmd))
    
    @classmethod
    def getHazardLevelCityGroup(cls, req):
        if len(req.selected) == 0:
            return None
        with Tr_Session() as session:
            join = " INNER JOIN "
            generalCmd = """select orders.city,orders.count general_count,coalesce(untreated.count,0) general_untreatedCount,coalesce(processed.count,0) general_processedCount, orders.discover_time discover_time from  
                (select city,count(*) count, any_value(discover_time) as discover_time from `order_list` where risk_level = '一般' group by city) orders 
                left join (select city,count(*) count from `order_list` where is_top_end = 0 and risk_level = '一般' group by city) untreated 
                on orders.city = untreated.city 
                left join (select city,count(*) count from `order_list` where is_top_end = 1 and risk_level = '一般' group by city) processed 
                on orders.city = processed.city """
            emergencyCmd = """select orders.city,orders.count emergency_count,coalesce(untreated.count,0) emergency_untreatedCount,coalesce(processed.count,0) emergency_processedCount, orders.discover_time from  
                (select city,count(*) count, any_value(discover_time) as discover_time from `order_list` where risk_level = '紧急' group by city) orders 
                left join (select city,count(*) count from `order_list` where is_top_end = 0 and risk_level = '紧急' group by city) untreated 
                on orders.city = untreated.city 
                left join (select city,count(*) count from `order_list` where is_top_end = 1 and risk_level = '紧急' group by city) processed 
                on orders.city = processed.city """
            if "二干/省内骨干网" not in req.selected:
                joinStr = join_arr(req.selected)
                generalCmd += f" where orders.city in {joinStr}"
                emergencyCmd += f" where orders.city in {joinStr}"
            generalCmd += ";"
            emergencyCmd += ";"
            generalData = session.execute(text(generalCmd))
            emergencyData = session.execute(text(emergencyCmd))
            if generalData.rowcount > emergencyData.rowcount:
                join = " LEFT JOIN "
            elif generalData.rowcount < emergencyData.rowcount:
                join = " RIGHT JOIN "
            cmd = """select IFNULL(general.city, emergency.city) city,coalesce(general.general_count,0) general_count,coalesce(general.general_untreatedCount,0) general_untreatedCount,coalesce(general.general_processedCount,0) general_processedCount, 
                coalesce(emergency.emergency_count,0) emergency_count,coalesce(emergency.emergency_untreatedCount,0) emergency_untreatedCount,coalesce(emergency.emergency_processedCount,0) emergency_processedCount 
                from (select orders.city,orders.count general_count,coalesce(untreated.count,0) general_untreatedCount,coalesce(processed.count,0) general_processedCount, orders.discover_time discover_time from  
                (select city,count(*) count, any_value(discover_time) as discover_time from `order_list` where risk_level = '一般' group by city) orders 
                left join (select city,count(*) count from `order_list` where is_top_end = 0 and risk_level = '一般' group by city) untreated 
                on orders.city = untreated.city 
                left join (select city,count(*) count from `order_list` where is_top_end = 1 and risk_level = '一般' group by city) processed 
                on orders.city = processed.city) general """ + join + """ (select orders.city,orders.count emergency_count,coalesce(untreated.count,0) emergency_untreatedCount,coalesce(processed.count,0) emergency_processedCount, orders.discover_time from  
                (select city,count(*) count, any_value(discover_time) as discover_time from `order_list` where risk_level = '紧急' group by city) orders 
                left join (select city,count(*) count from `order_list` where is_top_end = 0 and risk_level = '紧急' group by city) untreated 
                on orders.city = untreated.city 
                left join (select city,count(*) count from `order_list` where is_top_end = 1 and risk_level = '紧急' group by city) processed 
                on orders.city = processed.city) emergency 
                on general.city = emergency.city"""
            if (req.timesArr.startTime != "" and req.timesArr.startTime):
                cmd += f" and (general.discover_time between '{req.timesArr.startTime}' and '{req.timesArr.endTime}') and (emergency.discover_time between '{req.timesArr.startTime}' and '{req.timesArr.endTime}')"
            if (len(req.selected) and ("二干/省内骨干网" not in req.selected)):
                joinStr = join_arr(req.selected)
                cmd += f" where general.city in {joinStr} or emergency.city in {joinStr} AND (general.city != '' or emergency.city != '');"
            else:
                cmd += " where (general.city != '' and emergency.city != '');"
            return session.execute(text(cmd))

    @classmethod
    def getHazardLevelDistrictGroup(cls, req):
        with Tr_Session() as session:
            join = " INNER JOIN "
            generalCmd = f"""select orders.district_county,orders.count general_count,coalesce(untreated.count,0) general_untreatedCount,coalesce(processed.count,0) general_processedCount, orders.discover_time from  
                (select district_county,count(*) count, any_value(discover_time) as discover_time from order_list where risk_level = '一般' and city = '{req.city}' group by district_county) orders 
                left join (select district_county,count(*) count from order_list where is_top_end = 0 and risk_level = '一般' and city = '{req.city}' group by district_county) untreated 
                on orders.district_county = untreated.district_county 
                left join (select district_county,count(*) count from order_list where is_top_end = 1 and risk_level = '一般' and city = '{req.city}' group by district_county) processed 
                on orders.district_county = processed.district_county;
            """
            emergencyCmd = f"""select orders.district_county,orders.count emergency_count,coalesce(untreated.count,0) emergency_untreatedCount,coalesce(processed.count,0) emergency_processedCount, orders.discover_time from  
                (select district_county,count(*) count, any_value(discover_time) as discover_time from order_list where risk_level = '紧急' and city = '{req.city}' group by district_county) orders 
                left join (select district_county,count(*) count from order_list where is_top_end = 0 and risk_level = '紧急' and city = '{req.city}' group by district_county) untreated 
                on orders.district_county = untreated.district_county 
                left join (select district_county,count(*) count from order_list where is_top_end = 1 and risk_level = '紧急' and city = '{req.city}' group by district_county) processed 
                on orders.district_county = processed.district_county;
            """
            generalData = session.execute(text(generalCmd))
            emergencyData = session.execute(text(emergencyCmd))
            if generalData.rowcount > emergencyData.rowcount:
                join = " LEFT JOIN "
            elif generalData.rowcount < emergencyData.rowcount:
                join = " RIGHT JOIN "
            cmd = f"""select IFNULL(general.district_county, emergency.district_county) district_county,
                coalesce(general.general_count,0) general_count,coalesce(general.general_untreatedCount,0) general_untreatedCount,coalesce(general.general_processedCount,0) general_processedCount, 
                coalesce(emergency.emergency_count,0) emergency_count,coalesce(emergency.emergency_untreatedCount,0) emergency_untreatedCount,coalesce(emergency.emergency_processedCount,0) emergency_processedCount 
                from (select orders.district_county,orders.count general_count,coalesce(untreated.count,0) general_untreatedCount,coalesce(processed.count,0) general_processedCount, orders.discover_time from  
                (select district_county,count(*) count, any_value(discover_time) as discover_time from order_list where risk_level = '一般' and city = '{req.city}' group by district_county) orders 
                left join (select district_county,count(*) count from order_list where is_top_end = 0 and risk_level = '一般' and city = '{req.city}' group by district_county) untreated 
                on orders.district_county = untreated.district_county 
                left join (select district_county,count(*) count from order_list where is_top_end = 1 and risk_level = '一般' and city = '{req.city}' group by district_county) processed 
                on orders.district_county = processed.district_county) general 
                """ + join + f""" (select orders.district_county,orders.count emergency_count,coalesce(untreated.count,0) emergency_untreatedCount,coalesce(processed.count,0) emergency_processedCount, orders.discover_time from  
                (select district_county,count(*) count, any_value(discover_time) as discover_time from order_list where risk_level = '紧急' and city = '{req.city}' group by district_county) orders 
                left join (select district_county,count(*) count from order_list where is_top_end = 0 and risk_level = '紧急' and city = '{req.city}' group by district_county) untreated 
                on orders.district_county = untreated.district_county 
                left join (select district_county,count(*) count from order_list where is_top_end = 1 and risk_level = '紧急' and city = '{req.city}' group by district_county) processed 
                on orders.district_county = processed.district_county) emergency 
                on general.district_county = emergency.district_county
            """
            if (req.startTime != "" and req.startTime != None):
                cmd += f" and (general.discover_time between '{req.startTime}' and '{req.endTime}') and (emergency.discover_time between '{req.startTime}' and '{req.endTime}');"
            else:
                cmd += ";"
            return session.execute(text(cmd))


def get_all_order_list():
    return OrderList.all()


def get_order_list_filter():
    return OrderList.all_for_filter()


def get_order_list_filter_later_part():
    return OrderList.all_for_filter_later_part()


def get_filter_citys(citys):
    return OrderList.get_city_filter(citys)


if __name__ == "__main__":
    filter = OrderList.get_filter(city=["保定市"])
    for it in filter:
        print(it[0], it[1], it[2], it[3], it[4])
