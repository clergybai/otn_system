import sqlalchemy as sa
from datetime import datetime
from common.database import EmptyModel, tr_session
import uuid


class CalcOtmBusinessWaves(EmptyModel):
    __tablename__ = "calc_otm_business_waves"

    id = sa.Column(sa.VARCHAR(63), primary_key=True, nullable=False)
    source_ne_id = sa.Column(sa.VARCHAR(63), default=None)
    source_oa_shelf_id = sa.Column(sa.VARCHAR(63), default=None)
    source_oa_slot_id = sa.Column(sa.VARCHAR(63), default=None)
    source_oa_fingerprint = sa.Column(sa.VARCHAR(127), nullable=False)
    target_ne_id = sa.Column(sa.VARCHAR(63), default=None)
    target_oa_shelf_id = sa.Column(sa.VARCHAR(63), default=None)
    target_oa_slot_id = sa.Column(sa.VARCHAR(63), default=None)
    target_oa_fingerprint = sa.Column(sa.VARCHAR(127), default=None)
    business_waves = sa.Column(sa.Integer, default=None)
    oms_source_id = sa.Column(sa.VARCHAR(63), default=None)
    oms_target_id = sa.Column(sa.VARCHAR(63), default=None)
    oms_source_sub_name = sa.Column(sa.VARCHAR(63), default=None)
    oms_target_sub_name = sa.Column(sa.VARCHAR(63), default=None)
    sys_name = sa.Column(sa.VARCHAR(63), default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer, default=0)

    def __init__(self, source_ne_id, source_oa_shelf_id, source_oa_slot_id, source_oa_fingerprint,
                 target_ne_id, target_oa_shelf_id, target_oa_slot_id, target_oa_fingerprint,
                 business_waves, oms_source_id, oms_target_id, oms_source_sub_name, oms_target_sub_name,
                 sys_name, timestamp=datetime.now(), is_history=2):
        self.id = str(uuid.uuid4())
        self.source_ne_id = source_ne_id
        self.source_oa_shelf_id = source_oa_shelf_id
        self.source_oa_slot_id = source_oa_slot_id
        self.source_oa_fingerprint = source_oa_fingerprint
        self.target_ne_id = target_ne_id
        self.target_oa_shelf_id = target_oa_shelf_id
        self.target_oa_slot_id = target_oa_slot_id
        self.target_oa_fingerprint = target_oa_fingerprint
        self.business_waves = business_waves
        self.oms_source_id = oms_source_id
        self.oms_target_id = oms_target_id
        self.oms_source_sub_name = oms_source_sub_name
        self.oms_target_sub_name = oms_target_sub_name
        self.sys_name = sys_name
        self.timestamp = timestamp
        self.is_history = is_history

    @classmethod
    def get(cls, **kwargs):
        return tr_session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def bulk_add(cls, kwargs_list):
        calc_otm_business_waves_list = []
        for kwargs in kwargs_list:
            calc_otm_business_waves = cls(**kwargs)
            calc_otm_business_waves_list.append(calc_otm_business_waves)
        if len(calc_otm_business_waves_list) > 0:
            tr_session.add_all(calc_otm_business_waves_list)
            tr_session.commit()
