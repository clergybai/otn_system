import sqlalchemy as sa
from datetime import datetime
from common.database import EmptyModel, tr_session


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

    @classmethod
    def update(cls, filters, **kwargs):
        return tr_session.query(cls).filter_by(**filters).update(**kwargs)
