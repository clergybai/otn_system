import sqlalchemy as sa
import uuid
from datetime import datetime
from common.database import EmptyModel, tr_session


class ComputingMode(EmptyModel):
    __tablename__ = "computing_mode"

    id = sa.Column(sa.VARCHAR(63), primary_key=True)
    sys_name = sa.Column(sa.VARCHAR(255), nullable=True)
    state = sa.Column(sa.Integer)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer)

    def __init__(self, sys_name, state, timestamp=datetime.now(), is_history=0):
        self.id = str(uuid.uuid4())
        self.age = sys_name
        self.state = state
        self.timestamp = timestamp
        self.is_history = is_history

    @classmethod
    def get_computed_state(cls):
        # stmt = sa.text(f"SELECT state FROM {cls.__tablename__};")
        # return tr_session.execute(stmt).scalar()
        return tr_session.query(cls.state).first()[0]

    @classmethod
    def add(cls, **kwargs):
        mode = cls(**kwargs)
        tr_session.add(mode)
        tr_session.commit()
        return mode

    @classmethod
    def update(cls, filters, **kwargs):
        return tr_session.query(cls).filter_by(**filters).update(**kwargs)

    @classmethod
    def get_all_computing_mode(cls):
        return tr_session.query(cls).all()
