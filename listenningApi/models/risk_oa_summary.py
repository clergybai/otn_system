import sqlalchemy as sa
from sqlalchemy import column
from datetime import datetime
from common.database import EmptyModel, tr_session
import uuid


class RiskOaSummary(EmptyModel):
    __tablename__ = "risk_oa_summary"
    
    id = sa.Column(sa.VARCHAR(63), primary_key=True, nullable=False)
    city = sa.Column(sa.VARCHAR(63), default=None)
    net_level = sa.Column(sa.VARCHAR(63), default=None)
    source_ne_id = sa.Column(sa.VARCHAR(63), default=None)
    source_oa_shelf_id = sa.Column(sa.VARCHAR(63), default=None)
    source_oa_slot_id = sa.Column(sa.VARCHAR(63), default=None)
    oa_output_power_std_dev_risk = sa.Column(sa.Double, default=None)
    standard_wave_output = sa.Column(sa.Double, default=None)
    is_output_power_dev_risk = sa.Column(sa.VARCHAR(63), default=None)
    is_output_power_dev_emergency = sa.Column(sa.VARCHAR(63), default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer, default=0)

    def __init__(self, city, net_level, source_ne_id, source_oa_shelf_id, source_oa_slot_id,
                 oa_output_power_std_dev_risk, standard_wave_output, is_output_power_dev_risk,
                 is_output_power_dev_emergency, timestamp=datetime.now(), is_history=2):
        self.id = str(uuid.uuid4())
        self.city = city
        self.net_level = net_level
        self.source_ne_id = source_ne_id
        self.source_oa_shelf_id = source_oa_shelf_id
        self.source_oa_slot_id = source_oa_slot_id
        self.oa_output_power_std_dev_risk = oa_output_power_std_dev_risk
        self.standard_wave_output = standard_wave_output
        self.is_output_power_dev_risk = is_output_power_dev_risk
        self.is_output_power_dev_emergency = is_output_power_dev_emergency
        self.timestamp = timestamp,
        self.is_history = is_history
        
    @classmethod
    def get(cls, **kwargs):
        return tr_session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def bulk_add(cls, kwargs_list):
        risk_oa_summary_list = []
        for kwargs in kwargs_list:
            risk_oa_summary = cls(**kwargs)
            risk_oa_summary_list.append(risk_oa_summary)
        if len(risk_oa_summary_list) > 0:
            tr_session.add_all(risk_oa_summary_list)
            tr_session.commit()

    @classmethod
    def get_all_except(cls, except_cond, include_cond) -> list:
        query = tr_session.query(cls).filter_by(**include_cond)
        for key, val in except_cond.items():
            column_expr = column(key)
            query = query.filter(column_expr != val)
        return query.all()
