import sqlalchemy as sa
import uuid
from datetime import datetime
from webapi.database import EmptyModel
from webapi.database import db_trnas_session


class FrontAdj(EmptyModel):
    __tablename__ = 'front_adj'

    id = sa.Column(sa.VARCHAR(63), primary_key=True)
    source_ne_id = sa.Column(sa.VARCHAR(63), default=None)
    target_ne_id = sa.Column(sa.VARCHAR(63), default=None)
    source_sub_name = sa.Column(sa.VARCHAR(63), default=None)
    target_sub_name = sa.Column(sa.VARCHAR(63), default=None)
    source_ne_type = sa.Column(sa.VARCHAR(63), default=None)
    target_ne_type = sa.Column(sa.VARCHAR(63), default=None)
    sys_name = sa.Column(sa.VARCHAR(63), default=None)
    act_stand = sa.Column(sa.VARCHAR(63), default=None)
    fiber_length = sa.Column(sa.Integer, default=0)
    source_ne_color = sa.Column(sa.Integer, default=0)
    target_ne_color = sa.Column(sa.Integer, default=0)
    fiber_color = sa.Column(sa.Integer, default=0)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer, default=0)

    def __init__(self, source_ne_id, target_ne_id, source_sub_name,
                 target_sub_name, source_ne_type, target_ne_type,
                 sys_name, act_stand, fiber_length, source_ne_color,
                 target_ne_color, fiber_color, timestamp, is_history):
        self.id = str(uuid.uuid4())
        self.source_ne_id = source_ne_id
        self.target_ne_id = target_ne_id
        self.source_sub_name = source_sub_name
        self.target_sub_name = target_sub_name
        self.source_ne_type = source_ne_type
        self.target_ne_type = target_ne_type
        self.sys_name = sys_name
        self.act_stand = act_stand
        self.fiber_length = fiber_length
        self.source_ne_color = source_ne_color
        self.target_ne_color = target_ne_color
        self.fiber_color = fiber_color
        self.timestamp = timestamp
        self.is_history = is_history

    @classmethod
    def get_front_adjs(cls, **kwargs):
        return db_trnas_session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def bulk_add(cls, kwargs_list):
        data_list = []
        for kwargs in kwargs_list:
            data = cls(**kwargs)
            data_list.append(data)
        if len(data_list) > 0:
            db_trnas_session.add_all(data_list)
            db_trnas_session.commit()
