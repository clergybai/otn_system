import sqlalchemy as sa
from datetime import datetime
from common.database import EmptyModel, tr_session
import uuid


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
    
    def __init__(self, net_level, sys_name, act_stand, city, a_ne_id, a_shelf_id,
                 a_slot_id, a_in_out_id, a_sub_name, a_oa_fingerprint, a_oa_dir_fingerprint,
                 z_ne_id, z_shelf_id, z_slot_id, z_in_out_id, z_sub_name, z_oa_fingerprint,
                 z_oa_dir_fingerprint, full_waves, fiber_name, fiber_length, timestamp=datetime.now(),
                 is_history=2):
        self.id = str(uuid.uuid4())
        self.net_level = net_level
        self.sys_name = sys_name
        self.act_stand = act_stand
        self.city = city
        self.a_ne_id = a_ne_id
        self.a_shelf_id = a_shelf_id
        self.a_slot_id = a_slot_id
        self.a_in_out_id = a_in_out_id
        self.a_sub_name = a_sub_name
        self.a_oa_fingerprint = a_oa_fingerprint
        self.a_oa_dir_fingerprint = a_oa_dir_fingerprint
        self.z_ne_id = z_ne_id
        self.z_shelf_id = z_shelf_id
        self.z_slot_id = z_slot_id
        self.z_in_out_id = z_in_out_id
        self.z_sub_name = z_sub_name
        self.z_oa_fingerprint = z_oa_fingerprint
        self.z_oa_dir_fingerprint = z_oa_dir_fingerprint
        self.full_waves = full_waves
        self.fiber_name = fiber_name
        self.fiber_length = fiber_length
        self.timestamp = timestamp
        self.is_history = is_history

    @classmethod
    def update(cls, filters, **kwargs):
        return tr_session.query(cls).filter_by(**filters).update(**kwargs)

    @classmethod
    def get(cls, **kwargs):
        return tr_session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def distincet_get(cls, **kwargs):
        return tr_session.query(cls).filter_by(**kwargs).distinct().all()

    @classmethod
    def bulk_add(cls, kwargs_list):
        input_top_data_list = []
        for kwargs in kwargs_list:
            input_top_data = cls(**kwargs)
            input_top_data_list.append(input_top_data)
        if len(input_top_data_list) > 0:
            tr_session.add_all(input_top_data_list)
            tr_session.commit()
