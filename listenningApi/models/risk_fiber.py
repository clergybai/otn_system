import sqlalchemy as sa
from sqlalchemy import column
from datetime import datetime
from common.database import EmptyModel, tr_session
import uuid


class RiskFiber(EmptyModel):
    __tablename__ = "risk_fiber"
    
    id = sa.Column(sa.VARCHAR(63), primary_key=True, nullable=False)
    source_ne_id = sa.Column(sa.VARCHAR(63), default=None)
    target_ne_id = sa.Column(sa.VARCHAR(63), default=None)
    act_stand = sa.Column(sa.VARCHAR(63), default=None)
    fiber_loss_1 = sa.Column(sa.Double, default=None)
    fiber_loss_2 = sa.Column(sa.Double, default=None)
    fiber_two_way_dev_risk = sa.Column(sa.Double, default=None)
    cable_in_out_baseline = sa.Column(sa.Double, default=None)
    is_risk = sa.Column(sa.VARCHAR(63), default=None)
    is_emergency = sa.Column(sa.VARCHAR(63), default=None)
    city = sa.Column(sa.VARCHAR(63), default=None)
    net_level = sa.Column(sa.VARCHAR(63), default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer, default=0)
    
    def __init__(self, source_ne_id, target_ne_id, act_stand, fiber_loss_1, fiber_loss_2,
                 fiber_two_way_dev_risk, cable_in_out_baseline, is_risk, is_emergency, city,
                 net_level, timestamp=datetime.now(), is_history=2):
        self.id = str(uuid.uuid4())
        self.source_ne_id = source_ne_id
        self.target_ne_id = target_ne_id
        self.act_stand = act_stand
        self.fiber_loss_1 = fiber_loss_1
        self.fiber_loss_2 = fiber_loss_2
        self.fiber_two_way_dev_risk = fiber_two_way_dev_risk
        self.cable_in_out_baseline = cable_in_out_baseline
        self.is_risk = is_risk
        self.is_emergency = is_emergency
        self.city = city
        self.net_level
        self.timestamp = timestamp
        self.is_history = is_history

    @classmethod
    def get(cls, **kwargs):
        return tr_session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def bulk_add(cls, kwargs_list):
        risk_fiber_list = []
        for kwargs in kwargs_list:
            risk_fiber = cls(**kwargs)
            risk_fiber_list.append(risk_fiber)
        if len(risk_fiber_list) > 0:
            tr_session.add_all(risk_fiber_list)
            tr_session.commit()

    @classmethod
    def get_all_except(cls, except_cond, include_cond) -> list:
        query = tr_session.query(cls).filter_by(**include_cond)
        for key, val in except_cond.items():
            column_expr = column(key)
            query = query.filter(column_expr != val)
        return query.all()
