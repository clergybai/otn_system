import sqlalchemy as sa
from datetime import datetime
from common.database import EmptyModel, tr_session
import uuid


class CalcOaPower(EmptyModel):
    __tablename__ = "calc_oa_power"

    id = sa.Column(sa.VARCHAR(63), primary_key=True, nullable=False)
    source_ne_id = sa.Column(sa.VARCHAR(63), default=None)
    source_oa_shelf_id = sa.Column(sa.VARCHAR(63), default=None)
    source_oa_slot_id = sa.Column(sa.VARCHAR(63), default=None)
    internal_voa = sa.Column(sa.Double, default=None)
    outerside_voa = sa.Column(sa.Double, default=None)
    incoming_power = sa.Column(sa.Double, default=None)
    outing_power = sa.Column(sa.Double, default=None)
    is_voa_back = sa.Column(sa.Integer, default=0)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer, default=0)
    
    def __init__(self, source_ne_id, source_oa_shelf_id, source_oa_slot_id, internal_voa,
                 outerside_voa, incoming_power, outing_power, is_voa_back,
                 timestamp=datetime.now(), is_history=2):
        self.id = str(uuid.uuid4())
        self.source_ne_id = source_ne_id
        self.source_oa_shelf_id = source_oa_shelf_id,
        self.source_oa_slot_id = source_oa_slot_id,
        self.internal_voa = internal_voa
        self.outerside_voa = outerside_voa,
        self.incoming_power = incoming_power
        self.outing_power = outing_power
        self.is_voa_back = is_voa_back
        self.timestamp = timestamp
        self.is_history = is_history

    @classmethod
    def get(cls, **kwargs):
        return tr_session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def bulk_add(cls, kwargs_list):
        calc_oa_power_list = []
        for kwargs in kwargs_list:
            calc_oa_power = cls(**kwargs)
            calc_oa_power_list.append(calc_oa_power)
        if len(calc_oa_power_list) > 0:
            tr_session.add_all(calc_oa_power_list)
            tr_session.commit()
