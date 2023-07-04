import sqlalchemy as sa
from datetime import datetime
from common.database import EmptyModel, tr_session


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

    @classmethod
    def update(cls, filters, **kwargs):
        return tr_session.query(cls).filter_by(**filters).update(**kwargs)
