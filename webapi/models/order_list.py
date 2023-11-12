import sqlalchemy as sa
import uuid
from common.database import EmptyModel
from common.database import Tr_Session

import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


__all__ = ['OrderList']


class OrderList(EmptyModel):
    __tablename__ = 'order_list'

    id = sa.Column(sa.VARCHAR(63), primary_key=True)
    order_id = sa.Column(sa.VARCHAR(63))
    risk_id = sa.Column(sa.VARCHAR(63), nullable=False)
    risk_hash = sa.Column(sa.VARCHAR(63))
    source_ne_id = sa.Column(sa.VARCHAR(63))
    source_ne_sub_name = sa.Column(sa.VARCHAR(63))
    source_shelf_id = sa.Column(sa.VARCHAR(63))
    source_slot_id = sa.Column(sa.VARCHAR(63))
    target_ne_id = sa.Column(sa.VARCHAR(63))
    target_ne_sub_name = sa.Column(sa.VARCHAR(63))
    city = sa.Column(sa.VARCHAR(63))
    district_county = sa.Column(sa.VARCHAR(63))
    sys_name = sa.Column(sa.VARCHAR(63))
    oms = sa.Column(sa.VARCHAR(63))
    network_level = sa.Column(sa.VARCHAR(63))
    manufactor = sa.Column(sa.VARCHAR(63))
    risk_level = sa.Column(sa.VARCHAR(63))
    risk_type = sa.Column(sa.VARCHAR(63))
    risk_content = sa.Column(sa.VARCHAR(63))
    current_value = sa.Column(sa.Float)
    standard_value = sa.Column(sa.Float)
    unit_measurement = sa.Column(sa.VARCHAR(7))
    discover_time = sa.Column(sa.DateTime)
    is_send_top = sa.Column(sa.Integer)
    is_top_end = sa.Column(sa.Integer)
    top_feedback_message = sa.Column(sa.VARCHAR(63))
    top_order_end_time = sa.Column(sa.DateTime)
    timestamp = sa.Column(sa.DateTime, nullable=False)
    is_history = sa.Column(sa.Integer)

    def __init(self, order_id, risk_id, risk_hash,
               source_ne_id, source_ne_sub_name, source_shelf_id,
               source_slot_id, target_ne_id, target_ne_sub_name,
               city, district_county, sys_name, oms,
               network_level, manufactor, risk_level,
               risk_type, risk_content, current_value,
               standard_value, unit_measurement, discover_time,
               is_send_top, is_top_end, top_feedback_message,
               top_order_end_time, timestamp, is_history):
        self.id = str(uuid.uuid4())
        self.order_id = order_id
        self.risk_id = risk_id
        self.risk_hash = risk_hash
        self.source_ne_id = source_ne_id
        self.source_ne_sub_name = source_ne_sub_name
        self.source_shelf_id = source_shelf_id
        self.source_slot_id = source_slot_id
        self.target_ne_id = target_ne_id
        self.target_ne_sub_name = target_ne_sub_name
        self.city = city
        self.district_county = district_county
        self.sys_name = sys_name
        self.oms = oms
        self.network_level = network_level
        self.manufactor = manufactor
        self.risk_level = risk_level
        self.risk_type = risk_type
        self.risk_content = risk_content
        self.current_value = current_value
        self.standard_value = standard_value
        self.unit_measurement = unit_measurement
        self.discover_time = discover_time
        self.is_send_top = is_send_top
        self.is_top_end = is_top_end
        self.top_feedback_message = top_feedback_message
        self.top_order_end_time = top_order_end_time
        self.timestamp = timestamp
        self.is_history = is_history

    @classmethod
    def get_orders(cls, **kwargs):
        with Tr_Session() as session:
            return session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def all(cls):
        with Tr_Session() as session:
            return session.query(cls).all()

    @classmethod
    def all_for_filter(cls):
        with Tr_Session() as session:
            return session.query(
                cls.city,
                cls.district_county,
                cls.sys_name).distinct(
                    cls.district_county,
                    cls.city,
                    cls.sys_name).all()

    @classmethod
    def all_for_filter_later_part(cls):
        with Tr_Session() as session:
            return session.query(
                cls.network_level,
                cls.risk_level,
                cls.is_top_end,
                cls.is_send_top).distinct(
                    cls.network_level,
                    cls.risk_level,
                    cls.is_top_end,
                    cls.is_send_top).all()

    @classmethod
    def get_orders_by_time(cls, start, end, **kwargs):
        with Tr_Session() as session:
            return session.query(cls).\
                filter_by(**kwargs).\
                filter(cls.timestamp.between(start, end)).\
                order_by(cls.timestamp).all()

    @classmethod
    def get_filter(cls, **kwargs):
        with Tr_Session() as session:
            query = session.query(
                cls.city,
                cls.district_county,
                cls.sys_name,
                cls.network_level,
                cls.risk_level).distinct(
                    cls.district_county,
                    cls.city,
                    cls.sys_name,
                    cls.network_level,
                    cls.risk_level)
            return query.all()

    @classmethod
    def get_trouble_by_filter(cls, **kwargs):
        # 获取开始时间，结束时间
        start_time = None
        end_time = None
        order_id = None
        param = kwargs.get('param')
        city_list = []
        filter_city_list = False
        if param:
            times_arr = param.get('timesArr')
            if times_arr:
                start = times_arr.get('startTime')
                if start and len(start) > 0:
                    start_time = start
                end = times_arr.get('endTime')
                if end and len(end) > 0:
                    end_time = end
            selected = param.get('selected')
            if selected:
                city_list = selected
            order_id = param.get('order_id')

        # query = db_trnas_session.query(cls).filter(cls.is_history == 0)
        with Tr_Session() as session:
            query = session.query(cls)

            if order_id and len(order_id) > 0:
                query = query.filter(cls.order_id.like('%'+order_id+'%'))
            if start_time:
                query = query.filter(cls.discover_time >= start_time)
            if end_time:
                query = query.filter(cls.discover_time < end_time)

            # handle filter
            filters = kwargs.get("filter")
            if filters:
                for item in filters:
                    if len(item.items()) > 0:
                        name = item.get('name')
                        if name == 'city':
                            filter_city_list = True
                            city_list = item.get('values')
                        elif name:
                            query.filter(getattr(cls, name).in_(item.get('values')))

            if filter_city_list:
                query = query.filter(getattr(cls, 'city').in_(city_list))
            # handle page_index and page size
            page_idx = kwargs.get('page_index_begin')
            page_size = kwargs.get('page_size')

            total = query.count()
            # order by discovery time desc
            query = query.order_by(sa.desc(cls.discover_time))

            if page_idx is not None and page_size is not None:
                idx = 0 if (page_idx - 1) < 0 else page_idx - 1
                start = idx * page_size
                query = query.offset(start).limit(page_size)

            return (total, query.all())

    @classmethod
    def get_city_filter(cls, city_list):
        with Tr_Session() as session:
            return session.query(cls.district_county).filter(
                getattr(cls, 'city').in_(city_list)).distinct(
                    cls.district_county
                ).all()

    @classmethod
    def bulk_add(cls, kwargs_list):
        order_list = []
        for kwargs in kwargs_list:
            order = cls(**kwargs)
            order_list.append(order)
        if len(order_list) > 0:
            with Tr_Session() as session:
                try:
                    session.add_all(order_list)
                    session.commit()
                except Exception as e:
                    session.rollback()
                    raise e
