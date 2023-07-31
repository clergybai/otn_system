import sqlalchemy as sa
from datetime import datetime
from common.database import EmptyModel, tr_session
import uuid


class CalcOlaBusinessWaves(EmptyModel):
    __tablename__ = "calc_ola_business_waves"
    
    id = sa.Column(sa.VARCHAR(63), primary_key=True, nullable=False)
    ola_ne_id = sa.Column(sa.VARCHAR(63), nullable=False)
    business_waves = sa.Column(sa.Integer, default=None)
    oms_source_id = sa.Column(sa.VARCHAR(63), default=None)
    oms_target_id = sa.Column(sa.VARCHAR(63), default=None)
    oms_source_sub_name = sa.Column(sa.VARCHAR(63), default=None)
    oms_target_sub_name = sa.Column(sa.VARCHAR(63), default=None)
    sys_name = sa.Column(sa.VARCHAR(63), default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer, default=0)
    
    def __init__(self, ola_ne_id, business_waves, oms_source_id, oms_target_id,
                 oms_source_sub_name, oms_target_sub_name, sys_name,
                 timestamp=datetime.now(), is_history=2):
        self.id = str(uuid.uuid4())
        self.ola_ne_id = ola_ne_id
        self.business_waves = business_waves
        self.oms_source_id = oms_source_id
        self.oms_target_id = oms_target_id
        self.oms_source_sub_name = oms_source_sub_name
        self.oms_target_sub_name = oms_target_sub_name
        self.sys_name = sys_name
        self.timestamp = timestamp
        self.is_history = is_history

    @classmethod
    def get(cls, **kwargs):
        return tr_session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def bulk_add(cls, kwargs_list):
        calc_ola_business_waves_list = []
        for kwargs in kwargs_list:
            calc_ola_business_waves = cls(**kwargs)
            calc_ola_business_waves_list.append(calc_ola_business_waves)
        if len(calc_ola_business_waves_list) > 0:
            tr_session.add_all(calc_ola_business_waves_list)
            tr_session.commit()
