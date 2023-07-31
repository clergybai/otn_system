import sqlalchemy as sa
import uuid
from datetime import datetime
from common.database import EmptyModel, tr_session


class CalcNeAdj(EmptyModel):
    __tablename__ = "calc_ne_adj"

    id = sa.Column(sa.VARCHAR(63), primary_key=True)
    source_ne_id = sa.Column(sa.VARCHAR(63), default=None)
    target_ne_id = sa.Column(sa.VARCHAR(63), default=None)
    source_sub_name = sa.Column(sa.VARCHAR(63), default=None)
    target_sub_name = sa.Column(sa.VARCHAR(63), default=None)
    act_stand = sa.Column(sa.VARCHAR(63), default=None)
    full_waves = sa.Column(sa.INTEGER, default=None)
    sys_name = sa.Column(sa.VARCHAR(63), default=None)
    fiber_name = sa.Column(sa.Text, default=None)
    fiber_length = sa.Column(sa.INTEGER, default=None)
    net_level = sa.Column(sa.VARCHAR(63), default=None)
    source_ne_type = sa.Column(sa.VARCHAR(63), default=None)
    target_ne_type = sa.Column(sa.VARCHAR(63), default=None)
    stand_fiber_loss = sa.Column(sa.Float, default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer, default=0)

    def __init__(self, source_ne_id, target_ne_id, source_sub_name, target_sub_name,
                 act_stand, full_waves, sys_name, fiber_name, fiber_length, net_level,
                 source_ne_type, target_ne_type, stand_fiber_loss, timestamp=datetime.now(),
                 is_history=2):
        self.id = str(uuid.uuid4())
        self.source_ne_id = source_ne_id
        self.target_ne_id = target_ne_id
        self.source_sub_name = source_sub_name
        self.target_sub_name = target_sub_name
        self.act_stand = act_stand
        self.full_waves = full_waves
        self.sys_name = sys_name
        self.fiber_name = fiber_name
        self.fiber_length = fiber_length
        self.net_level = net_level
        self.source_ne_type = source_ne_type
        self.target_ne_type = target_ne_type
        self.stand_fiber_loss = stand_fiber_loss
        self.is_history = is_history

    @classmethod
    def get(cls, **kwargs):
        return tr_session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def bulk_add(cls, kwargs_list):
        calc_ne_adj_list = []
        for kwargs in kwargs_list:
            input_top_data = cls(**kwargs)
            calc_ne_adj_list.append(input_top_data)
        if len(calc_ne_adj_list) > 0:
            tr_session.add_all(calc_ne_adj_list)
            tr_session.commit()
