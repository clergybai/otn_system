import sqlalchemy as sa
from datetime import datetime
from common.database import EmptyModel, tr_session
import uuid


class InputInternalTopology(EmptyModel):
    __tablename__ = "input_internal_topology"

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
    
    def __init__(self, a_sub_name, a_ne_id, a_shelf_id, a_slot_id,
                 a_port_id, a_in_out_id, a_board_model, z_sub_name,
                 z_ne_id, z_shelf_id, z_slot_id, z_port_id, z_in_out_id,
                 z_board_model, timestamp=datetime.now(), is_history=2):
        self.id = str(uuid.uuid4())
        self.a_sub_name = a_sub_name
        self.a_ne_id = a_ne_id
        self.a_shelf_id = a_shelf_id
        self.a_slot_id = a_slot_id
        self.a_port_id = a_port_id
        self.a_in_out_id = a_in_out_id
        self.a_board_model = a_board_model
        self.z_sub_name = z_sub_name
        self.z_ne_id = z_ne_id
        self.z_shelf_id = z_shelf_id
        self.z_slot_id = z_slot_id
        self.z_port_id = z_port_id
        self.z_in_out_id = z_in_out_id
        self.z_board_model = z_board_model
        self.timestamp = timestamp
        self.is_history = is_history

    @classmethod
    def get(cls, **kwargs):
        return tr_session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def update(cls, filters, **kwargs):
        return tr_session.query(cls).filter_by(**filters).update(**kwargs)

    @classmethod
    def bulk_add(cls, kwargs_list):
        input_internal_topology_list = []
        for kwargs in kwargs_list:
            input_top_data = cls(**kwargs)
            input_internal_topology_list.append(input_top_data)
        if len(input_internal_topology_list) > 0:
            tr_session.add_all(input_internal_topology_list)
            tr_session.commit()
