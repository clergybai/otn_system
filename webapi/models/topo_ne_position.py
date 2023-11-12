import sqlalchemy as sa
import uuid
from common.database import EmptyModel
from common.database import Tr_Session
import logging


logger = logging.getLogger(__name__)


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
        with Tr_Session(expire_on_commit=False) as session:
            return session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def update(cls, filters, **kwargs):
        with Tr_Session() as session:
            try:
                count = session.query(cls).filter_by(**filters).update(kwargs)
                session.commit()
                return count
            except Exception as e:
                logger.error(e)
                session.rollback()
                raise e

    @classmethod
    def bulk_add(cls, kwargs_list):
        input_top_data_list = []
        for kwargs in kwargs_list:
            input_top_data = cls(**kwargs)
            input_top_data_list.append(input_top_data)
        if len(input_top_data_list) > 0:
            with Tr_Session() as session:
                try:
                    session.add_all(input_top_data_list)
                    session.commit()
                except Exception as e:
                    logger.error(e)
                    session.rollback()
                    raise e
