import sqlalchemy as sa
from datetime import datetime
from common.database import EmptyModel, tr_session
import uuid


class InputVoaBackData(EmptyModel):
    __tablename__ = "input_voa_back_data"

    id = sa.Column(sa.VARCHAR(63), primary_key=True, nullable=False)
    ne_id = sa.Column(sa.VARCHAR(63), default=None)
    shelf_id = sa.Column(sa.VARCHAR(63), default=None)
    slot_id = sa.Column(sa.VARCHAR(63), default=None)
    vo = sa.Column(sa.INTEGER, default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer, default=0)

    def __init__(self, ne_id, shelf_id, slot_id, vo, timestamp=datetime.now(), is_history=2):
        self.id = str(uuid.uuid4())
        self.ne_id = ne_id
        self.shelf_id = shelf_id
        self.slot_id = slot_id
        self.vo = vo
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
        input_voa_back_data_list = []
        for kwargs in kwargs_list:
            input_voa_back_data = cls(**kwargs)
            input_voa_back_data_list.append(input_voa_back_data)
        if len(input_voa_back_data_list) > 0:
            tr_session.add_all(input_voa_back_data_list)
            tr_session.commit()
