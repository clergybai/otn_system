import sqlalchemy as sa
from datetime import datetime
from common.database import EmptyModel, tr_session
import uuid


class FrontPictureOtm(EmptyModel):
    __tablename__ = "front_picture_otm"
    
    id = sa.Column(sa.VARCHAR(63), primary_key=True, nullable=False)
    source_ne_id = sa.Column(sa.VARCHAR(63), nullable=False)
    ne_type = sa.Column(sa.VARCHAR(63), default=None)
    directions = sa.Column(sa.VARCHAR(63), default=None)
    is_olp = sa.Column(sa.VARCHAR(63), default=None)
    picture_id = sa.Column(sa.VARCHAR(127), default=None)
    direction_1 = sa.Column(sa.VARCHAR(127), default=None)
    direction_2 = sa.Column(sa.VARCHAR(127), default=None)
    direction_3 = sa.Column(sa.VARCHAR(127), default=None)
    direction_4 = sa.Column(sa.VARCHAR(127), default=None)
    direction_5 = sa.Column(sa.VARCHAR(127), default=None)
    direction_6 = sa.Column(sa.VARCHAR(127), default=None)
    direction_7 = sa.Column(sa.VARCHAR(127), default=None)
    direction_8 = sa.Column(sa.VARCHAR(127), default=None)
    direction_1_in_oa_fingerprint = sa.Column(sa.VARCHAR(127), default=None)
    direction_2_in_oa_fingerprint = sa.Column(sa.VARCHAR(127), default=None)
    direction_3_in_oa_fingerprint = sa.Column(sa.VARCHAR(127), default=None)
    direction_4_in_oa_fingerprint = sa.Column(sa.VARCHAR(127), default=None)
    direction_5_in_oa_fingerprint = sa.Column(sa.VARCHAR(127), default=None)
    direction_6_in_oa_fingerprint = sa.Column(sa.VARCHAR(127), default=None)
    direction_7_in_oa_fingerprint = sa.Column(sa.VARCHAR(127), default=None)
    direction_8_in_oa_fingerprint = sa.Column(sa.VARCHAR(127), default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer, default=0)
    
    def __init__(self, source_ne_id, ne_type, directions, is_olp, picture_id,
                 direction_1, direction_2, direction_3, direction_4, direction_5,
                 direction_6, direction_7, direction_8, direction_1_in_oa_fingerprint,
                 direction_2_in_oa_fingerprint, direction_3_in_oa_fingerprint,
                 direction_4_in_oa_fingerprint, direction_5_in_oa_fingerprint,
                 direction_6_in_oa_fingerprint, direction_7_in_oa_fingerprint,
                 direction_8_in_oa_fingerprint, timestamp=datetime.now(), is_history=2):
        self.id = str(uuid.uuid4())
        self.source_ne_id = source_ne_id
        self.ne_type = ne_type
        self.directions = directions
        self.is_olp = is_olp
        self.picture_id = picture_id
        self.direction_1 = direction_1
        self.direction_2 = direction_2
        self.direction_3 = direction_3
        self.direction_4 = direction_4
        self.direction_5 = direction_5
        self.direction_6 = direction_6
        self.direction_7 = direction_7
        self.direction_8 = direction_8
        self.direction_1_in_oa_fingerprint = direction_1_in_oa_fingerprint
        self.direction_2_in_oa_fingerprint = direction_2_in_oa_fingerprint
        self.direction_3_in_oa_fingerprint = direction_3_in_oa_fingerprint
        self.direction_4_in_oa_fingerprint = direction_4_in_oa_fingerprint
        self.direction_5_in_oa_fingerprint = direction_5_in_oa_fingerprint
        self.direction_6_in_oa_fingerprint = direction_6_in_oa_fingerprint
        self.direction_7_in_oa_fingerprint = direction_7_in_oa_fingerprint
        self.direction_8_in_oa_fingerprint = direction_8_in_oa_fingerprint
        self.timestamp = timestamp,
        self.is_history = is_history

    @classmethod
    def get(cls, **kwargs):
        return tr_session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def bulk_add(cls, kwargs_list):
        front_picture_otm_list = []
        for kwargs in kwargs_list:
            front_picture_otm = cls(**kwargs)
            front_picture_otm_list.append(front_picture_otm)
        if len(front_picture_otm_list) > 0:
            tr_session.add_all(front_picture_otm_list)
            tr_session.commit()
