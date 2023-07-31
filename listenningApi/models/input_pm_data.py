import sqlalchemy as sa
from datetime import datetime
from common.database import EmptyModel, tr_session
import uuid


class InputPmData(EmptyModel):
    __tablename__ = "input_pm_data"

    id = sa.Column(sa.VARCHAR(63), primary_key=True, nullable=False)
    sub_name = sa.Column(sa.VARCHAR(255), default=None)
    a_ne_id = sa.Column(sa.VARCHAR(63), default=None)
    shelf_id = sa.Column(sa.VARCHAR(63), default=None)
    slot_id = sa.Column(sa.VARCHAR(63), default=None)
    port_name = sa.Column(sa.VARCHAR(255), default=None)
    out_power = sa.Column(sa.Float, default=None)
    in_power = sa.Column(sa.Float, default=None)
    out_power_max = sa.Column(sa.Float, default=None)
    out_power_min = sa.Column(sa.Float, default=None)
    in_power_max = sa.Column(sa.Float, default=None)
    in_power_min = sa.Column(sa.Float, default=None)
    voa_vaule = sa.Column(sa.Float, default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer)

    def __init__(self, sub_name, a_ne_id, shelf_id, slot_id,
                 port_name, out_power, in_power, out_power_max, out_power_min,
                 in_power_max, in_power_min, voa_vaule, timestamp=datetime.now(), is_history=2):
        self.id = str(uuid.uuid4())
        self.sub_name = sub_name,
        self.a_ne_id = a_ne_id,
        self.shelf_id = shelf_id,
        self.slot_id = slot_id,
        self.port_name = port_name,
        self.out_power = out_power,
        self.in_power = in_power,
        self.out_power_max = out_power_max,
        self.out_power_min = out_power_min,
        self.in_power_max = in_power_max,
        self.in_power_min = in_power_min,
        self.voa_vaule = voa_vaule,
        self.timestamp = timestamp,
        self.is_history = is_history

    @classmethod
    def get(cls, **kwargs):
        return tr_session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def update(cls, filters, **kwargs):
        return tr_session.query(cls).filter_by(**filters).update(**kwargs)

    @classmethod
    def bulk_add(cls, kwargs_list):
        input_pm_data_list = []
        for kwargs in kwargs_list:
            input_pm_data = cls(**kwargs)
            input_pm_data_list.append(input_pm_data)
        if len(input_pm_data_list) > 0:
            tr_session.add_all(input_pm_data_list)
            tr_session.commit()
