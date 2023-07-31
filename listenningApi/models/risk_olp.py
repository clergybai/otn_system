import sqlalchemy as sa
from sqlalchemy import column
from datetime import datetime
from common.database import EmptyModel, tr_session
import uuid


class RiskOlp(EmptyModel):
    __tablename__ = "risk_olp"

    id = sa.Column(sa.VARCHAR(63), primary_key=True, nullable=False)
    olp_ne_id = sa.Column(sa.VARCHAR(63), default=None)
    olp_shelf_id = sa.Column(sa.VARCHAR(63), default=None)
    olp_slot_id = sa.Column(sa.VARCHAR(63), default=None)
    oa_ne_id_1 = sa.Column(sa.VARCHAR(63), default=None)
    oa_shelf_id_1 = sa.Column(sa.VARCHAR(63), default=None)
    oa_slot_id_1 = sa.Column(sa.VARCHAR(63), default=None)
    oa_ne_id_2 = sa.Column(sa.VARCHAR(63), default=None)
    oa_shelf_id_2 = sa.Column(sa.VARCHAR(63), default=None)
    oa_slot_id_2 = sa.Column(sa.VARCHAR(63), default=None)
    olp_power_dev_risk = sa.Column(sa.Double, default=None)
    olp_act_stand_baseline = sa.Column(sa.Double, default=None)
    is_risk = sa.Column(sa.VARCHAR(63), default=None)
    is_emergency = sa.Column(sa.VARCHAR(63), default=None)
    city = sa.Column(sa.VARCHAR(63), default=None)
    net_level = sa.Column(sa.VARCHAR(63), default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer, default=0)
    
    
    def __init__(self, olp_ne_id, olp_shelf_id, olp_slot_id, oa_ne_id_1, oa_shelf_id_1,
                 oa_slot_id_1, oa_ne_id_2, oa_shelf_id_2, oa_slot_id_2, olp_power_dev_risk,
                 olp_act_stand_baseline, is_risk, is_emergency, city, net_level,
                 timestamp=datetime.now(), is_history=2):
        self.id = str(uuid.uuid4())
        self.olp_ne_id = olp_ne_id
        self.olp_shelf_id = olp_shelf_id
        self.olp_slot_id = olp_slot_id
        self.oa_ne_id_1 = oa_ne_id_1
        self.oa_shelf_id_1 = oa_shelf_id_1
        self.oa_slot_id_1 = oa_slot_id_1
        self.oa_ne_id_2 = oa_ne_id_2
        self.oa_shelf_id_2 = oa_shelf_id_2
        self.oa_slot_id_2 = oa_slot_id_2
        self.olp_power_dev_risk = olp_power_dev_risk
        self.olp_act_stand_baseline = olp_act_stand_baseline
        self.is_risk = is_risk
        self.is_emergency = is_emergency
        self.city = city
        self.net_level = net_level
        self.timestamp = timestamp,
        self.is_history = is_history

    @classmethod
    def get(cls, **kwargs):
        return tr_session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def bulk_add(cls, kwargs_list):
        risk_olp_list = []
        for kwargs in kwargs_list:
            risk_olp = cls(**kwargs)
            risk_olp_list.append(risk_olp)
        if len(risk_olp_list) > 0:
            tr_session.add_all(risk_olp_list)
            tr_session.commit()

    @classmethod
    def get_all_except(cls, except_cond, include_cond) -> list:
        query = tr_session.query(cls).filter_by(**include_cond)
        for key, val in except_cond.items():
            column_expr = column(key)
            query = query.filter(column_expr != val)
        return query.all()
