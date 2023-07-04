import sqlalchemy as sa
from datetime import datetime
from common.database import EmptyModel, tr_session


class InputVoaBackData(EmptyModel):
    __tablename__ = "input_voa_back_data"

    id = sa.Column(sa.VARCHAR(63), primary_key=True, nullable=False)
    ne_id = sa.Column(sa.VARCHAR(63), default=None)
    shelf_id = sa.Column(sa.VARCHAR(63), default=None)
    slot_id = sa.Column(sa.VARCHAR(63), default=None)
    vo = sa.Column(sa.INTEGER, default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer, default=0)

    @classmethod
    def update(cls, filters, **kwargs):
        return tr_session.query(cls).filter_by(**filters).update(**kwargs)
