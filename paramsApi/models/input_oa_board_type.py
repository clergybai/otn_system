import sqlalchemy as sa
import uuid
from datetime import datetime
from common.database import EmptyModel, tr_session


class InputOaBoardType(EmptyModel):
    __tablename__ = "input_oa_board_type"

    id = sa.Column(sa.VARCHAR(63), primary_key=True)
    sub_id = sa.Column(sa.VARCHAR(63), default=None)
    sub_name = sa.Column(sa.VARCHAR(255), default=None)
    ne_id = sa.Column(sa.VARCHAR(63), default=None)
    shelf_id = sa.Column(sa.VARCHAR(63), default=None)
    slot_id = sa.Column(sa.VARCHAR(63), default=None)
    board_model = sa.Column(sa.VARCHAR(63), default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer)

    def __init__(self, sub_id, sub_name, ne_id, shelf_id,
                 slot_id, board_model, timestamp, is_history):
        self.id = str(uuid.uuid4())
        self.sub_id = sub_id
        self.sub_name = sub_name
        self.ne_id = ne_id
        self.shelf_id = shelf_id
        self.slot_id = slot_id
        self.board_model = board_model
        self.timestamp = timestamp
        self.is_history = is_history

    @classmethod
    def get_input_oa_board_types(cls, **kwargs):
        return tr_session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def get_board_types_by_page_size(cls, history_val, page_idx, page_size, filters):
        idx = 0 if (page_idx - 1) < 0 else page_idx - 1
        start = idx * page_size
        if filters is None:
            return tr_session.query(cls).filter(cls.is_history > history_val).offset(start).limit(page_size).all()

        query = cls.generate_query(history_val, filters)
        return query.offset(start).limit(page_size).all()

    @classmethod
    def get_board_types_total(cls, history_val, filters):
        if filters is None:
            return tr_session.query(cls).filter(cls.is_history > history_val).count()
        else:
            query = cls.generate_query(history_val, filters)
            return query.count()

    @classmethod
    def generate_query(cls, history_val, filters):
        query = tr_session.query(cls).filter(cls.is_history > history_val)
        for filter in filters:
            if len(filter.items()):
                field_name = filter['name']
                values = filter['values']
                if isinstance(values, list):
                    query = query.filter(getattr(cls, field_name).in_(values))
                else:
                    query = query.filter_by(**{field_name: values})
        return query

    @classmethod
    def update(cls, filters, **kwargs):
        return tr_session.query(cls).filter_by(**filters).update(**kwargs)
