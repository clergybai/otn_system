import sqlalchemy as sa
import uuid
from datetime import datetime
from common.database import EmptyModel, Tr_Session


class InputPmMca(EmptyModel):
    __tablename__ = "input_pm_mca"

    id = sa.Column(sa.VARCHAR(63), primary_key=True)
    ne_id = sa.Column(sa.VARCHAR(63), default=None)
    sub_name = sa.Column(sa.VARCHAR(255), default=None)
    brd_name = sa.Column(sa.VARCHAR(255), default=None)
    shelf_id = sa.Column(sa.VARCHAR(63), default=None)
    slot_id = sa.Column(sa.VARCHAR(63), default=None)
    port_id = sa.Column(sa.VARCHAR(63), default=None)
    path_id = sa.Column(sa.VARCHAR(63), default=None)
    direction = sa.Column(sa.VARCHAR(255), default=None)
    och_power = sa.Column(sa.Float, default=None)
    manufactor = sa.Column(sa.VARCHAR(8), default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer)

    def __init__(self, ne_id, sub_name, brd_name, shelf_id, slot_id, port_id,
                 path_id, direction, och_power, manufactor, timestamp, is_history):
        self.id = str(uuid.uuid4())
        self.sub_name = sub_name
        self.brd_name = brd_name
        self.ne_id = ne_id
        self.shelf_id = shelf_id
        self.slot_id = slot_id
        self.port_id = port_id
        self.path_id = path_id
        self.direction = direction
        self.och_power = och_power
        self.manufactor = manufactor
        self.timestamp = timestamp
        self.is_history = is_history

    @classmethod
    def get(cls, page_size, **kwargs):
        with Tr_Session() as session:
            return session.query(cls).filter_by(**kwargs).limit(page_size).all()

    @classmethod
    def bulk_add(cls, kwargs_list):
        input_voa_config_list = []
        for kwargs in kwargs_list:
            input_top_data = cls(**kwargs)
            input_voa_config_list.append(input_top_data)
        if len(input_voa_config_list) > 0:
            with Tr_Session() as session:
                try:
                    session.add_all(input_voa_config_list)
                    session.commit()
                except Exception as e:
                    session.rollback()
                    raise e

    @classmethod
    def update(cls, filters, **kwargs):
        with Tr_Session() as session:
            try:
                return session.query(cls).filter_by(**filters).update(**kwargs)
            except Exception as e:
                session.rollback()
                raise e
