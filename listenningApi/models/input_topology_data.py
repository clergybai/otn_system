import sqlalchemy as sa
from datetime import datetime
from common.database import EmptyModel, tr_session


class InputTopologyData(EmptyModel):
    __tablename__ = "input_topology_data"

    id = sa.Column(sa.VARCHAR(63), primary_key=True, nullable=False)
    net_level = sa.Column(sa.VARCHAR(63), default=None)
    sys_name = sa.Column(sa.VARCHAR(63), default=None)
    act_stand = sa.Column(sa.VARCHAR(63), default=None)
    city = sa.Column(sa.VARCHAR(63), default=None)
    a_ne_id = sa.Column(sa.VARCHAR(63), default=None)
    a_shelf_id = sa.Column(sa.VARCHAR(63), default=None)
    a_slot_id = sa.Column(sa.VARCHAR(63), default=None)
    a_in_out_id = sa.Column(sa.VARCHAR(63), default=None)
    a_sub_name = sa.Column(sa.VARCHAR(255), default=None)
    a_oa_fingerprint = sa.Column(sa.VARCHAR(127), default=None)
    a_oa_dir_fingerprint = sa.Column(sa.VARCHAR(127), default=None)
    z_ne_id = sa.Column(sa.VARCHAR(63), default=None)
    z_shelf_id = sa.Column(sa.VARCHAR(63), default=None)
    z_slot_id = sa.Column(sa.VARCHAR(63), default=None)
    z_in_out_id = sa.Column(sa.VARCHAR(63), default=None)
    z_sub_name = sa.Column(sa.VARCHAR(255), default=None)
    z_oa_fingerprint = sa.Column(sa.VARCHAR(127), default=None)
    z_oa_dir_fingerprint = sa.Column(sa.VARCHAR(127), default=None)
    full_waves = sa.Column(sa.INTEGER, default=None)
    fiber_name = sa.Column(sa.Text, default=None)
    fiber_length = sa.Column(sa.INTEGER, default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer, default=0)

    @classmethod
    def update(cls, filters, **kwargs):
        return tr_session.query(cls).filter_by(**filters).update(**kwargs)
