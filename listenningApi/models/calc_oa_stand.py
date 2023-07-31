import sqlalchemy as sa
from datetime import datetime
from common.database import EmptyModel, tr_session
import uuid


class CalcOaStand(EmptyModel):
    __tablename__ = "calc_oa_stand"
    
    id = sa.Column(sa.VARCHAR(63), primary_key=True, nullable=False)
    oa_fingerprint = sa.Column(sa.VARCHAR(127), nullable=False)
    standard_gain_min = sa.Column(sa.Double, default=None)
    standard_gain_max = sa.Column(sa.Double, default=None)
    standard_wave_output = sa.Column(sa.Double, default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer, default=0)
    
    def __init__(self, oa_fingerprint, standard_gain_min, standard_gain_max, standard_wave_output,
                 timestamp=datetime.now(), is_history=2):
        self.id = str(uuid.uuid4())
        self.oa_fingerprint = oa_fingerprint
        self.standard_gain_min = standard_gain_min
        self.standard_gain_max = standard_gain_max
        self.standard_wave_output = standard_wave_output
        self.timestamp = timestamp
        self.is_history = is_history

    @classmethod
    def get(cls, **kwargs):
        return tr_session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def bulk_add(cls, kwargs_list):
        calc_oa_stand_list = []
        for kwargs in kwargs_list:
            calc_oa_stand = cls(**kwargs)
            calc_oa_stand_list.append(calc_oa_stand)
        if len(calc_oa_stand_list) > 0:
            tr_session.add_all(calc_oa_stand_list)
            tr_session.commit()
