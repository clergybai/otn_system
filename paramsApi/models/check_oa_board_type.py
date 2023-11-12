import sqlalchemy as sa
import uuid
from datetime import datetime
from common.database import EmptyModel, Tr_Session


class CheckOaBoardType(EmptyModel):
    __tablename__ = "check_oa_board_type"

    id = sa.Column(sa.VARCHAR(63), primary_key=True)
    sys_name = sa.Column(sa.VARCHAR(255), default=None)
    sub_name = sa.Column(sa.VARCHAR(255), default=None)
    ne_id = sa.Column(sa.VARCHAR(63), default=None)
    shelf_id = sa.Column(sa.VARCHAR(63), default=None)
    slot_id = sa.Column(sa.VARCHAR(63), default=None)
    board_model = sa.Column(sa.VARCHAR(63), nullable=True)
    data_error = sa.Column(sa.VARCHAR(255), default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer)

    def __init__(self, sys_name, sub_name, ne_id, shelf_id, slot_id,
                 board_model, data_error, timestamp, is_history):
        self.id = str(uuid.uuid4())
        self.sys_name = sys_name
        self.sub_name = sub_name
        self.ne_id = ne_id
        self.shelf_id = shelf_id
        self.slot_id = slot_id
        self.board_model = board_model
        self.data_error = data_error
        self.timestamp = timestamp
        self.is_history = is_history

    @classmethod
    def get(cls, **kwargs):
        with Tr_Session() as session:
            return session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def get_by_page_size(cls, history_val, page_idx, page_size, filters):
        idx = 0 if (page_idx - 1) < 0 else page_idx - 1
        start = idx * page_size
        with Tr_Session() as session:
            if filters is None:
                return session.query(cls).filter(
                    cls.is_history == history_val).offset(
                        start).limit(page_size).all()

            query = cls.generate_query(session, history_val, filters)
            return query.offset(start).limit(page_size).all()

    @classmethod
    def get_by_filter(cls, history_val, filters):
        with Tr_Session() as session:
            if filters is None:
                return session.query(cls).filter(
                    cls.is_history == history_val
                ).all()
        query = cls.generate_query(session, history_val, filters)
        return query.all()

    @classmethod
    def get_total(cls, history_val, filters):
        with Tr_Session() as session:
            if filters is None:
                return session.query(cls).filter(
                    cls.is_history == history_val).count()
            else:
                query = cls.generate_query(session, history_val, filters)
                return query.count()

    @classmethod
    def generate_query(cls, session, history_val, filters):
        query = session.query(cls).filter(cls.is_history == history_val)
        for filter in filters:
            if len(filter.items()):
                field_name = filter['name']
                values = filter['values']
                if isinstance(values, list):
                    query = query.filter(getattr(cls, field_name).in_(values))
                else:
                    query = query.filter(
                        getattr(cls, field_name).like('%'+values+'%'))
        return query

    @classmethod
    def update(cls, filters, **kwargs):
        with Tr_Session() as session:
            return session.query(cls).filter_by(**filters).update(**kwargs)

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
                    session.rollback()
                    raise e
