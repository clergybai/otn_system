import sqlalchemy as sa
from datetime import datetime
from common.database import EmptyModel, pg_session


class PgInputTopologyData(EmptyModel):
    __tablename__ = "pg_input_topology_data"

    id = sa.Column(sa.String, primary_key=True, nullable=False)
    net_level = sa.Column(sa.String)
    sys_name = sa.Column(sa.String)
    act_stand = sa.Column(sa.String)
    city = sa.Column(sa.String)
    a_ne_id = sa.Column(sa.String)
    a_shelf_id = sa.Column(sa.String)
    a_slot_id = sa.Column(sa.String)
    a_in_out_id = sa.Column(sa.String)
    a_sub_name = sa.Column(sa.String)
    a_oa_fingerprint = sa.Column(sa.String)
    a_oa_dir_fingerprint = sa.Column(sa.String)
    z_ne_id = sa.Column(sa.String)
    z_shelf_id = sa.Column(sa.String)
    z_slot_id = sa.Column(sa.String)
    z_in_out_id = sa.Column(sa.String)
    z_sub_name = sa.Column(sa.String)
    z_oa_fingerprint = sa.Column(sa.String)
    z_oa_dir_fingerprint = sa.Column(sa.String)
    full_waves = sa.Column(sa.Integer)
    fiber_name = sa.Column(sa.String)
    fiber_length = sa.Column(sa.Integer)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer)

    @classmethod
    def get_all(cls):
        return pg_session.query(cls).all()
