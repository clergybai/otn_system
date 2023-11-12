import sqlalchemy as sa
from sqlalchemy.inspection import inspect
import uuid
from datetime import datetime
from common.database import EmptyModel, Tr_Session


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
                 standard_single_96_wave_output, timestamp=datetime.now(), is_history=11):
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
        with Tr_Session() as session:
            return session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def get_distinct_oa_board_standards_filter(cls, **kwargs):
        with Tr_Session() as session:
            return session.query(cls.board_model).distinct(cls.board_model).all()

    @classmethod
    def get_board_by_page_size(cls, history_val, page_idx, page_size, filters):
        idx = 0 if (page_idx - 1) < 0 else page_idx - 1
        start = idx * page_size
        with Tr_Session() as session:
            if filters is None:
                return session.query(cls).filter(cls.is_history == history_val).offset(start).limit(page_size).all()

            query = cls.generate_query(session, history_val, filters)
            return query.offset(start).limit(page_size).all()

    @classmethod
    def get_board_total(cls, history_val, filters):
        with Tr_Session() as session:
            if filters is None:
                return session.query(cls).filter(cls.is_history == history_val).count()
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
                    query = query.filter_by(**{field_name: values})
        return query

    @classmethod
    def update(cls, filters, **kwargs):
        with Tr_Session() as session:
            return session.query(cls).filter_by(**filters).update(**kwargs)

    @classmethod
    def add(cls, **kwargs):
        input_oa_board_standard = cls(**kwargs)
        with Tr_Session() as session:
            try:
                session.add(input_oa_board_standard)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
        return input_oa_board_standard

    @classmethod
    def get_count(cls, **filters) -> int:
        with Tr_Session() as session:
            query = session.query(sa.func.count(inspect(cls).primary_key[0]))
            for key, value in filters.items():
                if isinstance(value, list):
                    query = query.filter(getattr(cls, key).in_(value))
                else:
                    query = query.filter_by(**{key: value})
            count = query.scalar()
            return count

    @classmethod
    def bulk_update(cls, update_mappings):
        with Tr_Session() as session:
            try:
                session.bulk_update_mappings(cls, update_mappings)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
