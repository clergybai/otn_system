import sqlalchemy as sa
import uuid
from datetime import datetime
from common.database import EmptyModel, Tr_Session


class CheckTopology(EmptyModel):
    __tablename__ = "check_topology"

    id = sa.Column(sa.VARCHAR(63), primary_key=True)
    sys_name = sa.Column(sa.VARCHAR(255), default=None)
    net_level = sa.Column(sa.VARCHAR(63), default=None)
    city = sa.Column(sa.VARCHAR(63), default=None)
    a_sub_name = sa.Column(sa.VARCHAR(255), default=None)
    z_sub_name = sa.Column(sa.VARCHAR(255), default=None)
    a_ne_id = sa.Column(sa.VARCHAR(63), default=None)
    z_ne_id = sa.Column(sa.VARCHAR(63), default=None)
    a_shelf_id = sa.Column(sa.VARCHAR(63), default=None)
    z_shelf_id = sa.Column(sa.VARCHAR(63), default=None)
    a_slot_id = sa.Column(sa.VARCHAR(63), default=None)
    z_slot_id = sa.Column(sa.VARCHAR(63), default=None)
    a_in_out_id = sa.Column(sa.VARCHAR(63), default=None)
    z_in_out_id = sa.Column(sa.VARCHAR(63), default=None)
    full_waves = sa.Column(sa.Integer, default=None)
    fiber_length = sa.Column(sa.Integer, default=None)
    data_error = sa.Column(sa.VARCHAR(255), default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer)

    def __init__(self, sys_name, net_level, city, a_sub_name, z_sub_name,
                 a_ne_id, z_ne_id, a_shelf_id, z_shelf_id, a_slot_id, z_slot_id,
                 a_in_out_id, z_in_out_id, full_waves, fiber_length, data_error,
                 timestamp, is_history):
        self.id = str(uuid.uuid4())
        self.sys_name = sys_name
        self.net_level = net_level
        self.city = city
        self.a_sub_name = a_sub_name
        self.z_sub_name = z_sub_name
        self.a_ne_id = a_ne_id
        self.z_ne_id = z_ne_id
        self.a_shelf_id = a_shelf_id
        self.z_shelf_id = z_shelf_id
        self.a_slot_id = a_slot_id
        self.z_slot_id = z_slot_id
        self.a_in_out_id = a_in_out_id
        self.z_in_out_id = z_in_out_id
        self.full_waves = full_waves
        self.fiber_length = fiber_length
        self.data_error = data_error
        self.timestamp = timestamp
        self.is_history = is_history

    @classmethod
    def get(cls, **kwargs):
        with Tr_Session() as session:
            return session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def get_by_page_size(cls, history_val, page_idx, page_size, filters):
        idx = 0 if (page_idx - 1) < 0 else page_idx - 1
        start = idx * page_size
        with Tr_Session() as session:
            if filters is None:
                return session.query(cls).filter(
                    cls.is_history == history_val).offset(
                        start).limit(page_size).all()

            query = cls.generate_query(session, history_val, filters)
            return query.offset(start).limit(page_size).all()

    @classmethod
    def get_by_filter(cls, history_val, filters):
        with Tr_Session() as session:
            if filters is None:
                return session.query(cls).filter(
                    cls.is_history == history_val
                ).all()
        query = cls.generate_query(session, history_val, filters)
        return query.all()

    @classmethod
    def get_total(cls, history_val, filters):
        with Tr_Session() as session:
            if filters is None:
                return session.query(cls).filter(
                    cls.is_history == history_val).count()
            else:
                query = cls.generate_query(session, history_val, filters)
                return query.count()

    @classmethod
    def generate_query(cls, session, history_val, filters):
        query = session.query(cls).filter(cls.is_history == history_val)
        for filter in filters:
            if len(filter.items()):
                field_name = filter['name']
                values = filter['values']
                if isinstance(values, list):
                    query = query.filter(getattr(cls, field_name).in_(values))
                else:
                    query = query.filter(
                        getattr(cls, field_name).like('%'+values+'%'))
        return query

    @classmethod
    def update(cls, filters, **kwargs):
        with Tr_Session() as session:
            return session.query(cls).filter_by(**filters).update(**kwargs)

    @classmethod
    def bulk_add(cls, kwargs_list):
        input_top_data_list = []
        for kwargs in kwargs_list:
            input_top_data = cls(**kwargs)
            input_top_data_list.append(input_top_data)
        if len(input_top_data_list) > 0:
            with Tr_Session() as session:
                try:
                    session.add_all(input_top_data_list)
                    session.commit()
                except Exception as e:
                    session.rollback()
                    raise e
