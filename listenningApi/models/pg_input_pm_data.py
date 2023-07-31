import sqlalchemy as sa
from datetime import datetime
from common.database import EmptyModel, pg_session


class PgInputPmData(EmptyModel):
    __tablename__ = "pg_input_pm_data"

    id = sa.Column(sa.String, primary_key=True, nullable=False)
    sub_name = sa.Column(sa.String)
    a_ne_id = sa.Column(sa.String)
    shelf_id = sa.Column(sa.String)
    slot_id = sa.Column(sa.String)
    port_name = sa.Column(sa.String)
    out_power = sa.Column(sa.Double)
    in_power = sa.Column(sa.Double)
    out_power_max = sa.Column(sa.Double)
    out_power_min = sa.Column(sa.Double)
    in_power_max = sa.Column(sa.Double)
    in_power_min = sa.Column(sa.Double)
    voa_vaule = sa.Column(sa.Double)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer)

    @classmethod
    def get_all(cls):
        return pg_session.query(cls).all()
