import sqlalchemy as sa
from datetime import datetime
from common.database import EmptyModel, tr_session
import uuid


class FrontDataOa(EmptyModel):
    __tablename__ = "front_data_oa"

    id = sa.Column(sa.VARCHAR(63), primary_key=True, nullable=False)
    ne_id = sa.Column(sa.VARCHAR(63), default=None)
    shelf_id = sa.Column(sa.VARCHAR(63), default=None)
    slot_id = sa.Column(sa.VARCHAR(63), default=None)
    outside_voa = sa.Column(sa.Double, default=None)
    inside_voa = sa.Column(sa.Double, default=None)
    input_power = sa.Column(sa.Double, default=None)
    input_stand_power = sa.Column(sa.Double, default=None)
    output_power = sa.Column(sa.Double, default=None)
    output_stand_power = sa.Column(sa.Double, default=None)
    gain = sa.Column(sa.Double, default=None)
    stand_gain_min = sa.Column(sa.Double, default=None)
    stand_gain_max = sa.Column(sa.Double, default=None)
    brd_type = sa.Column(sa.VARCHAR(63), default=None)
    wavs = sa.Column(sa.Integer, default=None)
    oms = sa.Column(sa.VARCHAR(63), default=None)
    oa_risk_num = sa.Column(sa.Integer, default=None)
    in_ne_subname = sa.Column(sa.VARCHAR(127), default=None)
    out_ne_subname = sa.Column(sa.VARCHAR(127), default=None)
    ne_incoming_power = sa.Column(sa.Double, default=None)
    ne_outing_power = sa.Column(sa.Double, default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer, default=0)
    back_internal_voa = sa.Column(sa.Double, default=None)

    def __init__(self, ne_id, shelf_id, slot_id, outside_voa, inside_voa,
                 input_power, input_stand_power, output_power, output_stand_power,
                 gain, stand_gain_min, stand_gain_max, brd_type, wavs, oms, oa_risk_num,
                 in_ne_subname, out_ne_subname, ne_incoming_power, ne_outing_power, back_internal_voa,
                 timestamp=datetime.now(), is_history=2):
        self.id = str(uuid.uuid4())
        self.ne_id = ne_id
        self.shelf_id = shelf_id
        self.slot_id = slot_id
        self.outside_voa = outside_voa
        self.inside_voa = inside_voa
        self.input_power = input_power
        self.input_stand_power = input_stand_power
        self.output_power = output_power
        self.output_stand_power = output_stand_power
        self.gain = gain
        self.stand_gain_min = stand_gain_min
        self.stand_gain_max = stand_gain_max
        self.brd_type = brd_type
        self.wavs = wavs
        self.oms = oms
        self.oa_risk_num = oa_risk_num
        self.in_ne_subname = in_ne_subname
        self.out_ne_subname = out_ne_subname
        self.ne_incoming_power = ne_incoming_power
        self.ne_outing_power = ne_outing_power
        self.back_internal_voa = back_internal_voa
        self.timestamp = timestamp
        self.is_history = is_history

    @classmethod
    def get(cls, **kwargs):
        return tr_session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def bulk_add(cls, kwargs_list):
        front_data_oa_list = []
        for kwargs in kwargs_list:
            front_data_oa = cls(**kwargs)
            front_data_oa_list.append(front_data_oa)
        if len(front_data_oa_list) > 0:
            tr_session.add_all(front_data_oa_list)
            tr_session.commit()
