import sqlalchemy as sa
from datetime import datetime
from common.database import EmptyModel, tr_session
import uuid


class FrontNe(EmptyModel):
    __tablename__ = "front_ne"
    
    id = sa.Column(sa.VARCHAR(63), primary_key=True, nullable=False)
    source_ne_id = sa.Column(sa.VARCHAR(63), default=None)
    source_oa_sub_name = sa.Column(sa.VARCHAR(63), default=None)
    source_oa_shelf_id = sa.Column(sa.VARCHAR(63), default=None)
    source_oa_slot_id = sa.Column(sa.VARCHAR(63), default=None)
    source_oa_in_out_id = sa.Column(sa.VARCHAR(63), default=None)
    source_oa_fingerprint = sa.Column(sa.VARCHAR(63), default=None)
    target_ne_id = sa.Column(sa.VARCHAR(63), nullable=False)
    target_oa_sub_name = sa.Column(sa.VARCHAR(255), default=None)
    target_oa_shelf_id = sa.Column(sa.VARCHAR(63), nullable=False)
    target_oa_slot_id = sa.Column(sa.VARCHAR(63), default=None)
    target_oa_in_out_id = sa.Column(sa.VARCHAR(63), default=None)
    target_oa_fingerprint = sa.Column(sa.VARCHAR(63), nullable=False)
    act_stand = sa.Column(sa.VARCHAR(63), default=None)
    sys_name = sa.Column(sa.VARCHAR(63), default=None)
    manufactor = sa.Column(sa.VARCHAR(63), default=None)
    ne_type = sa.Column(sa.VARCHAR(63), default=None)
    ne_model = sa.Column(sa.VARCHAR(63), default=None)
    oa_color = sa.Column(sa.Integer, default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer, default=0)
    
    def __init__(self, source_ne_id, source_oa_sub_name, source_oa_shelf_id, source_oa_slot_id,
                 source_oa_in_out_id, source_oa_fingerprint, target_ne_id, target_oa_sub_name,
                 target_oa_shelf_id, target_oa_slot_id, target_oa_in_out_id, target_oa_fingerprint,
                 act_stand, sys_name, manufactor, ne_type, ne_model, oa_color,
                 timestamp=datetime.now(), is_history=2):
        self.id = str(uuid.uuid4())
        self.source_ne_id = source_ne_id
        self.source_oa_sub_name = source_oa_sub_name
        self.source_oa_shelf_id = source_oa_shelf_id
        self.source_oa_slot_id = source_oa_slot_id
        self.source_oa_in_out_id = source_oa_in_out_id
        self.source_oa_fingerprint = source_oa_fingerprint
        self.target_ne_id = target_ne_id
        self.target_oa_sub_name = target_oa_sub_name
        self.target_oa_shelf_id = target_oa_shelf_id
        self.target_oa_slot_id = target_oa_slot_id
        self.target_oa_in_out_id = target_oa_in_out_id
        self.target_oa_fingerprint = target_oa_fingerprint
        self.act_stand = act_stand
        self.sys_name = sys_name
        self.manufactor = manufactor
        self.ne_type = ne_type
        self.ne_model = ne_model
        self.oa_color = oa_color
        self.timestamp = timestamp
        self.is_history = is_history

    @classmethod
    def get(cls, **kwargs):
        return tr_session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def bulk_add(cls, kwargs_list):
        data_list = []
        for kwargs in kwargs_list:
            data = cls(**kwargs)
            data_list.append(data)
        if len(data_list) > 0:
            tr_session.add_all(data_list)
            tr_session.commit()
