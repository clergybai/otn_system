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

    def __init__(self, sys_name, state, timestamp, is_history):
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
