import sqlalchemy as sa
import uuid
from datetime import datetime
from common.database import EmptyModel, tr_session


class InputOaBoardStandard(EmptyModel):
    __tablename__ = "input_oa_board_standard"

    id = sa.Column(sa.VARCHAR(63), primary_key=True)
    board_model = sa.Column(sa.VARCHAR(63), nullable=True)
    standard_gain_min = sa.Column(sa.Float, default=None)
    standard_gain_max = sa.Column(sa.Float, default=None)
    standard_single_40_wave_output = sa.Column(sa.Float, default=None)
    standard_single_80_wave_output = sa.Column(sa.Float, default=None)
    standard_single_96_wave_output = sa.Column(sa.Float, default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer)

    def __init__(self, board_model, standard_gain_min, standard_gain_max,
                 standard_single_40_wave_output, standard_single_80_wave_output,
                 standard_single_96_wave_output, timestamp, is_history):
        self.id = str(uuid.uuid4())
        self.board_model = board_model
        self.standard_gain_min = standard_gain_min
        self.standard_gain_max = standard_gain_max
        self.standard_single_40_wave_output = standard_single_40_wave_output
        self.standard_single_80_wave_output = standard_single_80_wave_output
        self.standard_single_96_wave_output = standard_single_96_wave_output
        self.timestamp = timestamp
        self.is_history = is_history

    @classmethod
    def get_input_oa_board_standards(cls, **kwargs):
        return tr_session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def get_board_by_page_size(cls, history_val, page_idx, page_size, filters):
        idx = 0 if (page_idx - 1) < 0 else page_idx - 1
        start = idx * page_size
        if filters is None:
            return tr_session.query(cls).filter(cls.is_history > history_val).offset(start).limit(page_size).all()

        query = cls.generate_query(history_val, filters)
        return query.offset(start).limit(page_size).all()

    @classmethod
    def get_board_total(cls, history_val, filters):
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
