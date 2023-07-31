import sqlalchemy as sa
from datetime import datetime
from common.database import EmptyModel, tr_session
import uuid


class FrontPictureOla(EmptyModel):
    __tablename__ = "front_picture_ola"
    
    id = sa.Column(sa.VARCHAR(63), primary_key=True, nullable=False)
    source_ne_id = sa.Column(sa.VARCHAR(63), nullable=False)
    source_oa_sub_name = sa.Column(sa.VARCHAR(255), default=None)
    in_target_ne_id = sa.Column(sa.VARCHAR(127), default=None)
    in_target_ne_name = sa.Column(sa.VARCHAR(255), default=None)
    in_oa_shelf_id = sa.Column(sa.VARCHAR(63), default=None)
    in_oa_slot_id = sa.Column(sa.VARCHAR(63), default=None)
    out_oa_shelf_id = sa.Column(sa.VARCHAR(63), default=None)
    out_oa_slot_id = sa.Column(sa.VARCHAR(63), default=None)
    oa_num = sa.Column(sa.Integer, default=0)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer, default=0)
    
    def __init__(self, source_ne_id, source_oa_sub_name, in_target_ne_id, in_target_ne_name,
                 in_oa_shelf_id, in_oa_slot_id, out_oa_shelf_id, out_oa_slot_id, oa_num,
                 timestamp=datetime.now(), is_history=2):
        self.id = str(uuid.uuid4())
        self.source_ne_id = source_ne_id
        self.source_oa_sub_name = source_oa_sub_name
        self.in_target_ne_id = in_target_ne_id
        self.in_target_ne_name = in_target_ne_name
        self.in_oa_shelf_id = in_oa_shelf_id
        self.in_oa_slot_id = in_oa_slot_id
        self.out_oa_shelf_id = out_oa_shelf_id
        self.out_oa_slot_id = out_oa_slot_id
        self.out_oa_shelf_id = out_oa_shelf_id
        self.oa_num = oa_num
        self.timestamp = timestamp
        self.is_history = is_history

    @classmethod
    def get(cls, **kwargs):
        return tr_session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def bulk_add(cls, kwargs_list):
        front_picture_ola_list = []
        for kwargs in kwargs_list:
            front_picture_ola = cls(**kwargs)
            front_picture_ola_list.append(front_picture_ola)
        if len(front_picture_ola_list) > 0:
            tr_session.add_all(front_picture_ola_list)
            tr_session.commit()
