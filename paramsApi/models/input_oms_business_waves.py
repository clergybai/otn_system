import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.inspection import inspect
import uuid
from datetime import datetime
from common.database import EmptyModel, Tr_Session


class InputOmsBusinessWaves(EmptyModel):
    __tablename__ = "input_oms_business_waves"

    id = sa.Column(sa.VARCHAR(63), primary_key=True)
    sys_name = sa.Column(sa.VARCHAR(63), default=None)
    net_level = sa.Column(sa.VARCHAR(63), default=None)
    city = sa.Column(sa.VARCHAR(63), default=None)
    a_sub_name = sa.Column(sa.VARCHAR(255), default=None)
    a_ne_id = sa.Column(sa.VARCHAR(63), default=None)
    z_sub_name = sa.Column(sa.VARCHAR(255), default=None)
    z_ne_id = sa.Column(sa.VARCHAR(63), default=None)
    business_waves = sa.Column(sa.INTEGER, default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer)

    def __init__(self, sys_name, net_level, city, a_sub_name,
                 a_ne_id, z_sub_name, z_ne_id, business_waves,
                 timestamp=datetime.now(), is_history=0):
        self.id = str(uuid.uuid4())
        self.sys_name = sys_name
        self.net_level = net_level
        self.city = city
        self.a_sub_name = a_sub_name
        self.a_ne_id = a_ne_id
        self.z_sub_name = z_sub_name
        self.z_ne_id = z_ne_id
        self.business_waves = business_waves
        self.timestamp = timestamp
        self.is_history = is_history

    @classmethod
    def get_filter(cls, **kwargs):
        with Tr_Session() as session:
            query = session.query(cls.sys_name, cls.city, cls.net_level)
            for key, val in kwargs.items():
                if isinstance(val, list):
                    query = query.filter(getattr(cls, key).in_(val))
                else:
                    query = query.filter_by(**{key: val})
            return query.all()

    @classmethod
    def get_input_oms_business_waves(cls, **kwargs):
        with Tr_Session() as session:
            return session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def get_oms_by_filter(cls, **kwargs):
        param = kwargs.get('param')
        city_list = []
        # filter_city_list = False
        if param:
            selected = param.get('selected')
            if selected:
                city_list = selected
        with Tr_Session() as session:
            query = session.query(cls)
            # handle filter
            filters = kwargs.get("filter")
            if filters:
                for item in filters:
                    if len(item.items()) > 0:
                        name = item.get('name')
                        if name == 'city':
                            city_list = item.get('values')
                        if name == 'sys_name':
                            sys_name_value = "%{}%".format(item.get('values')[0])
                            query = query.filter(cls.sys_name.like(sys_name_value))
                        elif name:
                            query = query.filter(getattr(cls, name).in_(item.get('values')))

            if len(city_list) > 0:
                query = query.filter(getattr(cls, 'city').in_(city_list))
            query = query.filter(cls.is_history == 0)
            page_idx = kwargs.get('page_index_begin')
            page_size = kwargs.get('page_size')
            total = query.count()
            # query = query.order_by(sa.asc(cls.sys_name))

            if page_idx is not None and page_size is not None:
                idx = 0 if (page_idx - 1) < 0 else page_idx - 1
                start = idx * page_size
                query = query.offset(start).limit(page_size)
            return (total, query.all())

    @classmethod
    def get_count(cls, **filters) -> int:
        with Tr_Session() as session:
            query = session.query(func.count(inspect(cls).primary_key[0]))
            for key, val in filters.items():
                if isinstance(val, list):
                    query = query.filter(getattr(cls, key).in_(val))
                else:
                    query = query.filter_by(**{key: val})
            count = query.scalar()
            return count

    @classmethod
    def execute_raw_sql(cls, sql_str):
        with Tr_Session() as session:
            query = session.execute(sql_str)
            return query.fetchall()

    @classmethod
    def delete(cls, **kwargs) -> bool:
        with Tr_Session() as session:
            rows_del = session.query(cls).filter_by(**kwargs).delete()
            return rows_del > 0

    @classmethod
    def update(cls, filters, **kwargs):
        with Tr_Session() as session:
            try:
                rows = session.query(cls).filter_by(**filters)
                rows_updated = rows.update(kwargs)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
        return rows_updated > 0

    @classmethod
    def add_input_oms_bizs(cls, input_oms_bizs):
        with Tr_Session() as session:
            try:
                session.add_all(input_oms_bizs)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    @classmethod
    def bulk_update(cls, update_mappings):
        with Tr_Session() as session:
            try:
                session.bulk_update_mappings(cls, update_mappings)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
