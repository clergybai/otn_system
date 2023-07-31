import sqlalchemy as sa
import uuid
from webapi.database import EmptyModel
from webapi.database import db_trnas_session


class TopoNePosition(EmptyModel):
    __tablename__ = 'topo_ne_position'

    id = sa.Column(sa.VARCHAR(63), primary_key=True)
    user_name = sa.Column(sa.VARCHAR(31), default=None)
    sys_name = sa.Column(sa.VARCHAR(63), default=None)
    ne_id = sa.Column(sa.VARCHAR(63), nullable=False)
    x = sa.Column(sa.VARCHAR(63), default=None)
    y = sa.Column(sa.VARCHAR(63), default=None)
    canvasx = sa.Column(sa.VARCHAR(63), default=None)
    canvasy = sa.Column(sa.VARCHAR(63), default=None)
    clientx = sa.Column(sa.VARCHAR(63), default=None)
    clienty = sa.Column(sa.VARCHAR(63), default=None)

    def __init__(self, user_name, sys_name, ne_id, x, y,
                 canvasx, canvasy, clientx, clienty):
        self.id = str(uuid.uuid4())
        self.user_name = user_name
        self.sys_name = sys_name
        self.ne_id = ne_id
        self.x = x
        self.y = y
        self.canvasx = canvasx
        self.canvasy = canvasy
        self.clientx = clientx
        self.clienty = clienty

    @classmethod
    def get_positions(cls, **kwargs):
        return db_trnas_session.query(cls).filter_by(**kwargs).all()
