import sqlalchemy as sa
from datetime import datetime
from common.database import EmptyModel, tr_session
import uuid


class CalcFibersSum(EmptyModel):
    __tablename__ = "calc_fibers_sum"

    id = sa.Column(sa.VARCHAR(63), primary_key=True, nullable=False)
    sys_name = sa.Column(sa.VARCHAR(63), default=None)
    act_stand = sa.Column(sa.VARCHAR(63), default=None)
    sum_fibers_length = sa.Column(sa.Integer, default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer, default=0)

    def __init__(self, sys_name, act_stand, sum_fibers_length, timestamp=datetime.now(), is_history=2):
        self.id = str(uuid.uuid4())
        self.sys_name = sys_name
        self.act_stand = act_stand
        self.sum_fibers_length = sum_fibers_length
        self.timestamp = timestamp
        self.is_history = is_history

    @classmethod
    def bulk_add(cls, kwargs_list):
        calc_fibers_sum_list = []
        for kwargs in kwargs_list:
            input_top_data = cls(**kwargs)
            calc_fibers_sum_list.append(input_top_data)
        if len(calc_fibers_sum_list) > 0:
            tr_session.add_all(calc_fibers_sum_list)
            tr_session.commit()
