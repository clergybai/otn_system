import sqlalchemy as sa
from datetime import datetime
from common.database import EmptyModel, tr_session
import uuid


class CalcNeOas(EmptyModel):
    __tablename__ = "calc_ne_oas"
    
    id = sa.Column(sa.VARCHAR(63), primary_key=True, nullable=False)
    source_ne_id = sa.Column(sa.VARCHAR(63), default=None)
    source_oa_sub_name = sa.Column(sa.VARCHAR(255), default=None)
    source_oa_shelf_id = sa.Column(sa.VARCHAR(63), default=None)
    source_oa_slot_id = sa.Column(sa.VARCHAR(63), default=None)
    source_oa_in_out_id = sa.Column(sa.VARCHAR(63), default=None)
    source_oa_fingerprint = sa.Column(sa.VARCHAR(127), default=None)
    source_oa_dir_fingerprint = sa.Column(sa.VARCHAR(127), nullable=False)
    target_ne_id = sa.Column(sa.VARCHAR(63), nullable=False)
    target_oa_sub_name = sa.Column(sa.VARCHAR(255), default=None)
    target_oa_shelf_id = sa.Column(sa.VARCHAR(63), nullable=False)
    target_oa_slot_id = sa.Column(sa.VARCHAR(63), default=None)
    target_oa_in_out_id = sa.Column(sa.VARCHAR(63), default=None)
    target_oa_fingerprint = sa.Column(sa.VARCHAR(127), nullable=False)
    target_oa_dir_fingerprint = sa.Column(sa.VARCHAR(127), default=None)
    act_stand = sa.Column(sa.VARCHAR(63), default=None)
    full_waves = sa.Column(sa.Integer, default=None)
    fiber_loss = sa.Column(sa.Double, default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer, default=0)
    
    def __init__(self, source_ne_id, source_oa_sub_name, source_oa_shelf_id, source_oa_slot_id,
                 source_oa_in_out_id, source_oa_fingerprint, source_oa_dir_fingerprint, target_ne_id,
                 target_oa_sub_name, target_oa_shelf_id, target_oa_slot_id, target_oa_in_out_id,
                 target_oa_fingerprint, target_oa_dir_fingerprint, act_stand, full_waves,
                 fiber_loss, timestamp=datetime.now(), is_history=2):
        self.id = str(uuid.uuid4())
        self.source_ne_id = source_ne_id
        self.source_oa_sub_name = source_oa_sub_name
        self.source_oa_shelf_id = source_oa_shelf_id
        self.source_oa_slot_id = source_oa_slot_id
        self.source_oa_in_out_id = source_oa_in_out_id
        self.source_oa_fingerprint = source_oa_fingerprint
        self.source_oa_dir_fingerprint = source_oa_dir_fingerprint
        self. target_ne_id = target_ne_id
        self.target_oa_sub_name = target_oa_sub_name
        self.target_oa_shelf_id = target_oa_shelf_id
        self.target_oa_slot_id = target_oa_slot_id
        self.target_oa_in_out_id = target_oa_in_out_id
        self.target_oa_fingerprint = target_oa_fingerprint
        self.target_oa_dir_fingerprint = target_oa_dir_fingerprint
        self.act_stand = act_stand
        self.full_waves = full_waves
        self.fiber_loss = fiber_loss
        self.timestamp = timestamp
        self.is_history = is_history

    @classmethod
    def get(cls, **kwargs):
        return tr_session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def bulk_add(cls, kwargs_list):
        calc_ne_oas_list = []
        for kwargs in kwargs_list:
            calc_ne_oas = cls(**kwargs)
            calc_ne_oas_list.append(calc_ne_oas)
        if len(calc_ne_oas_list) > 0:
            tr_session.add_all(calc_ne_oas_list)
            tr_session.commit()
