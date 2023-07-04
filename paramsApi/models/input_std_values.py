import sqlalchemy as sa
import uuid
from datetime import datetime
from common.database import EmptyModel, tr_session


class InputStdValues(EmptyModel):
    __tablename__ = "input_std_values"

    id = sa.Column(sa.VARCHAR(63), primary_key=True)
    optical_power_baseline = sa.Column(sa.Float, default=None)
    gain_baseline = sa.Column(sa.Float, default=None)
    olp_act_stand_baseline = sa.Column(sa.Float, default=None)
    cable_in_out_baseline = sa.Column(sa.Float, default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer)

    def __init__(self, optical_power_baseline, gain_baseline, olp_act_stand_baseline,
                 cable_in_out_baseline, timestamp, is_history):
        self.id = str(uuid.uuid4())
        self.optical_power_baseline = optical_power_baseline
        self.gain_baseline = gain_baseline
        self.olp_act_stand_baseline = olp_act_stand_baseline
        self.cable_in_out_baseline = cable_in_out_baseline
        self.timestamp = timestamp
        self.is_history = is_history

    @classmethod
    def get_input_std_value(cls, **kwargs):
        query = tr_session.query(cls).filter_by(**kwargs)
        return query.order_by(sa.desc(cls.timestamp)).first()
