import sqlalchemy as sa
from datetime import datetime
from common.database import EmptyModel, tr_session
import uuid


class InputOpticalNe(EmptyModel):
    __tablename__ = "input_optical_ne"

    id = sa.Column(sa.VARCHAR(63), primary_key=True, nullable=False)
    ne_id = sa.Column(sa.VARCHAR(63), nullable=False)
    ne_name = sa.Column(sa.VARCHAR(255), default=None)
    city = sa.Column(sa.VARCHAR(63), default=None)
    district_county = sa.Column(sa.VARCHAR(63), default=None)
    manufactor = sa.Column(sa.VARCHAR(63), default=None)
    network_level = sa.Column(sa.VARCHAR(63), default=None)
    ne_type = sa.Column(sa.VARCHAR(63), default=None)
    ne_model = sa.Column(sa.VARCHAR(63), default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer, default=0)

    def __init__(self, ne_id, ne_name, city, district_county, manufactor,
                 network_level, ne_type, ne_model, timestamp=datetime.now(), is_history=2):
        self.id = str(uuid.uuid4())
        self.ne_id = ne_id
        self.ne_name = ne_name
        self.city = city
        self.district_county = district_county
        self.manufactor = manufactor
        self.network_level = network_level
        self.ne_type = ne_type
        self.ne_model = ne_model
        self.timestamp = timestamp
        self.is_history = is_history

    @classmethod
    def get(cls, **kwargs):
        return tr_session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def update(cls, filters, **kwargs):
        rows_updated = tr_session.query(cls).filter_by(**filters).update(**kwargs)
        tr_session.commit()
        return rows_updated > 0

    @classmethod
    def bulk_add(cls, kwargs_list):
        input_optical_ne_list = []
        for kwargs in kwargs_list:
            input_optical_ne = cls(**kwargs)
            input_optical_ne_list.append(input_optical_ne)
        if len(input_optical_ne_list) > 0:
            tr_session.add_all(input_optical_ne_list)
            tr_session.commit()
