import sqlalchemy as sa
from datetime import datetime
from common.database import EmptyModel, tr_session


class InputInternalTopology(EmptyModel):
    __tabelename__ = "input_internal_topology"

    id = sa.Column(sa.VARCHAR(63), primary_key=True, nullable=False)
    a_sub_name = sa.Column(sa.VARCHAR(255), default=None)
    a_ne_id = sa.Column(sa.VARCHAR(63), default=None)
    a_shelf_id = sa.Column(sa.VARCHAR(63), default=None)
    a_slot_id = sa.Column(sa.VARCHAR(63), default=None)
    a_port_id = sa.Column(sa.VARCHAR(63), default=None)
    a_in_out_id = sa.Column(sa.VARCHAR(63), default=None)
    a_board_model = sa.Column(sa.VARCHAR(63), default=None)
    z_sub_name = sa.Column(sa.VARCHAR(255), default=None)
    z_ne_id = sa.Column(sa.VARCHAR(63), default=None)
    z_shelf_id = sa.Column(sa.VARCHAR(63), default=None)
    z_slot_id = sa.Column(sa.VARCHAR(63), default=None)
    z_port_id = sa.Column(sa.VARCHAR(63), default=None)
    z_in_out_id = sa.Column(sa.VARCHAR(63), default=None)
    z_board_model = sa.Column(sa.VARCHAR(63), default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer, default=0)

    @classmethod
    def update(cls, filters, **kwargs):
        return tr_session.query(cls).filter_by(**filters).update(**kwargs)
