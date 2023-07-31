from ..models.order_list import OrderList
import datetime
from dateutil.relativedelta import relativedelta


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
        
        print(f"total: {total}, items: {str(items)}")
        
        return total, [{
            'id': item.id,
            'order_id': item.order_id,
            'risk_id': item.risk_id,
            'risk_hash': item.risk_hash,
            'source_ne_id': item.source_ne_id,
            'source_ne_sub_name': item.source_ne_sub_name,
            'source_shelf_id': item.source_shelf_id,
            'source_slot_id': item.source_slot_id,
            'target_ne_id': item.target_ne_id,
            'target_ne_sub_name': item.target_ne_sub_name,
            'city': item.city,
            'district_county': item.district_county,
            'sys_name': item.sys_name,
            'oms': item.oms,
            'network_level': item.network_level,
            'manufactor': item.manufactor,
            'risk_level': item.risk_level,
            'risk_type': item.risk_type,
            'risk_content': item.risk_content,
            'current_value': item.current_value,
            'standard_value': item.standard_value,
            'unit_measurement': item.unit_measurement,
            'discover_time': item.discover_time,
            'is_send_top': item.is_send_top,
            'is_top_end': item.is_top_end,
            'top_feedback_message': item.top_feedback_message,
            'top_order_end_time': item.top_order_end_time,
            'timestamp': item.timestamp,
            'is_history': item.is_history
            } for item in items]


if __name__ == "__main__":
    filter = OrderList.get_filter(city=["保定市"])
    for it in filter:
        print(it[0], it[1], it[2], it[3], it[4])
