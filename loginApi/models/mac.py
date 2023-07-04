import sqlalchemy as sa
import datetime
from ..database import EmptyModel, lo_session


class Mac(EmptyModel):
    __tablename__ = 'mac'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    addr = sa.Column(sa.VARCHAR(255), nullable=False)
    key = sa.Column(sa.VARCHAR(1031), nullable=False)
    is_history = sa.Column(sa.Integer, nullable=False, default=0)
    create_time = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, addr, key, is_history=0):
        self.addr = addr
        self.key = key
        self.is_history = is_history

    def __repr__(self) -> str:
        return '<Mac {add}>'.format(add=self.addr)

    @classmethod
    def find_mac_by(cls, **kwargs):
        return lo_session.query(cls).filter_by(**kwargs).one_or_none()

    @classmethod
    def set_mac_record_to_history(cls, addr):
        row_updated = lo_session.query(cls).filter(cls.addr == addr).\
            update({"is_history": 1}, synchronize_session=False)
        lo_session.commit()
        if row_updated > 0:
            return True
        return False

    @classmethod
    def add_mac(cls, mac):
        lo_session.add(mac)
        lo_session.commit()
        return mac.id
