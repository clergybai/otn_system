import sqlalchemy as sa
from datetime import datetime
from webapi.database import EmptyModel
from webapi.database import db_trnas_session


class SystemLabel(EmptyModel):
    __tablename__ = 'system_label'

    id = sa.Column(sa.VARCHAR(63), primary_key=True)
    system_name = sa.Column(sa.VARCHAR(127), nullable=False)
    full_waves = sa.Column(sa.Integer, default=None)
    sys_atc_fiber_length = sa.Column(sa.Integer, default=None)
    sys_standby_fiber_length = sa.Column(sa.Integer, default=None)
    risk_sum = sa.Column(sa.Integer, default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer, default=0)

    def __init__(self, id, system_name, full_waves, sys_atc_fiber_length,
                 sys_standby_fiber_length, risk_sum, timestamp, is_history):
        self.id = id
        self.system_name = system_name
        self.full_waves = full_waves
        self.sys_atc_fiber_length = sys_atc_fiber_length
        self.sys_standby_fiber_length = sys_standby_fiber_length
        self.risk_sum = risk_sum
        self.timestamp = timestamp
        self.is_history = is_history

    @classmethod
    def get_system_label_first(cls, **kwargs):
        return db_trnas_session.query(cls).filter_by(**kwargs).first()

    @classmethod
    def bulk_add(cls, kwargs_list):
        data_list = []
        for kwargs in kwargs_list:
            data = cls(**kwargs)
            data_list.append(data)
        if len(data_list) > 0:
            db_trnas_session.add_all(data_list)
            db_trnas_session.commit()
