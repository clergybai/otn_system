import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.inspection import inspect
import uuid
from datetime import datetime
from common.database import EmptyModel, Tr_Session


class CalcOms(EmptyModel):
    __tablename__ = "calc_oms"
    
    id = sa.Column(sa.VARCHAR(63), primary_key=True)
    oms_id = sa.Column(sa.VARCHAR(63), nullable=False)
    sys_name = sa.Column(sa.VARCHAR(63), default=None)
    oms_source_id = sa.Column(sa.VARCHAR(63), default=None)
    oms_target_id = sa.Column(sa.VARCHAR(63), default=None)
    act_stand = sa.Column(sa.VARCHAR(63), default=None)
    business_waves = sa.Column(sa.INTEGER, default=None)
    full_waves = sa.Column(sa.INTEGER, default=None)
    ola_all = sa.Column(sa.VARCHAR(2047), default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer)
    
    def __init__(self, oms_id, sys_name, oms_source_id, oms_target_id,
                 act_stand, business_waves, full_waves, ola_all, timestamp=datetime.now(), is_history=2):
        self.id = str(uuid.uuid4())
        self.oms_id = oms_id,
        self.sys_name = sys_name
        self.oms_source_id = oms_source_id
        self.oms_target_id = oms_target_id
        self.act_stand = act_stand
        self.business_waves = business_waves
        self.full_waves = full_waves
        self.ola_all = ola_all
        self.timestamp = timestamp
        self.is_history = is_history

    @classmethod
    def get(cls, **kwargs):
        with Tr_Session() as session:
            return session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def bulk_add(cls, kwargs_list):
        calc_oms_list = []
        for kwargs in kwargs_list:
            calc_oms = cls(**kwargs)
            calc_oms_list.append(calc_oms)
        if len(calc_oms_list) > 0:
            with Tr_Session() as session:
                try:
                    session.add_all(calc_oms_list)
                    session.commit()
                except Exception as e:
                    session.rollback()
                    raise e
