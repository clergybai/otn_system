import sqlalchemy as sa
from datetime import datetime
from common.database import EmptyModel, tr_session
import uuid


class CalcIncomingOpticalPower(EmptyModel):
    __tablename__ = "calc_incoming_optical_power"

    id = sa.Column(sa.VARCHAR(63), primary_key=True, nullable=False)
    oa_fingerprint = sa.Column(sa.VARCHAR(127), nullable=False)
    incoming_optical_power = sa.Column(sa.Double, default=None)
    internal_voa = sa.Column(sa.Double, default=None)
    outside_voa = sa.Column(sa.Double, default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer, default=0)

    def __init__(self, oa_fingerprint, incoming_optical_power, internal_voa, outside_voa,
                 timestamp=datetime.now(), is_history=2):
        self.id = str(uuid.uuid4())
        self.oa_fingerprint = oa_fingerprint
        self.incoming_optical_power = incoming_optical_power
        self.internal_voa = internal_voa
        self.outside_voa = outside_voa
        self.timestamp = timestamp
        self.is_history = is_history

    @classmethod
    def get(cls, **kwargs):
        return tr_session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def bulk_add(cls, kwargs_list):
        calc_incoming_optical_power_list = []
        for kwargs in kwargs_list:
            calc_incoming_optical_power = cls(**kwargs)
            calc_incoming_optical_power_list.append(calc_incoming_optical_power)
        if len(calc_incoming_optical_power_list) > 0:
            tr_session.add_all(calc_incoming_optical_power_list)
            tr_session.commit()
