import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.inspection import inspect
from datetime import datetime
from common.database import EmptyModel, Tr_Session
import uuid


class InputThreshold(EmptyModel):
    __tablename__ = "input_threshold"

    id = sa.Column(sa.VARCHAR(63), primary_key=True)
    rule_name = sa.Column(sa.VARCHAR(63), default=None)
    city = sa.Column(sa.VARCHAR(63), default=None)
    net_level = sa.Column(sa.VARCHAR(63), default=None)
    owner = sa.Column(sa.VARCHAR(63), default=None)
    is_used = sa.Column(sa.INTEGER, default=None)
    oa_input_power_fluc_risk_thr = sa.Column(sa.INTEGER, default=None)
    oa_input_power_fluc_risk_maj = sa.Column(sa.INTEGER, default=None)
    oa_input_power_fluc_risk_urg = sa.Column(sa.INTEGER, default=None)
    oa_output_power_fluc_risk_thr = sa.Column(sa.INTEGER, default=None)
    oa_output_power_fluc_risk_maj = sa.Column(sa.INTEGER, default=None)
    oa_output_power_fluc_risk_urg = sa.Column(sa.INTEGER, default=None)
    oa_gain_std_dev_up_risk_thr = sa.Column(sa.INTEGER, default=None)
    oa_gain_std_dev_up_risk_maj = sa.Column(sa.INTEGER, default=None)
    oa_gain_std_dev_up_risk_urg = sa.Column(sa.INTEGER, default=None)
    oa_gain_std_dev_low_risk_thr = sa.Column(sa.INTEGER, default=None)
    oa_gain_std_dev_low_risk_maj = sa.Column(sa.INTEGER, default=None)
    oa_gain_std_dev_low_risk_urg = sa.Column(sa.INTEGER, default=None)
    oa_input_power_std_dev_up_risk_thr = sa.Column(sa.INTEGER, default=None)
    oa_input_power_std_dev_up_risk_maj = sa.Column(sa.INTEGER, default=None)
    oa_input_power_std_dev_up_risk_urg = sa.Column(sa.INTEGER, default=None)
    oa_input_power_std_dev_low_risk_thr = sa.Column(sa.INTEGER, default=None)
    oa_input_power_std_dev_low_risk_maj = sa.Column(sa.INTEGER, default=None)
    oa_input_power_std_dev_low_risk_urg = sa.Column(sa.INTEGER, default=None)
    oa_output_power_std_dev_up_risk_thr = sa.Column(sa.INTEGER, default=None)
    oa_output_power_std_dev_up_risk_maj = sa.Column(sa.INTEGER, default=None)
    oa_output_power_std_dev_up_risk_urg = sa.Column(sa.INTEGER, default=None)
    oa_output_power_std_dev_low_risk_thr = sa.Column(sa.INTEGER, default=None)
    oa_output_power_std_dev_low_risk_maj = sa.Column(sa.INTEGER, default=None)
    oa_output_power_std_dev_low_risk_urg = sa.Column(sa.INTEGER, default=None)
    fiber_two_way_dev_risk_thr = sa.Column(sa.INTEGER, default=None)
    fiber_two_way_dev_risk_maj = sa.Column(sa.INTEGER, default=None)
    fiber_two_way_dev_risk_urg = sa.Column(sa.INTEGER, default=None)
    olp_power_dev_risk_thr = sa.Column(sa.INTEGER, default=None)
    olp_power_dev_risk_maj = sa.Column(sa.INTEGER, default=None)
    olp_power_dev_risk_urg = sa.Column(sa.INTEGER, default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer)

    def __init__(self, rule_name, city, net_level, owner, is_used,
                 oa_input_power_fluc_risk_thr, oa_input_power_fluc_risk_maj,
                 oa_input_power_fluc_risk_urg, oa_output_power_fluc_risk_thr,
                 oa_output_power_fluc_risk_maj, oa_output_power_fluc_risk_urg,
                 oa_gain_std_dev_up_risk_thr, oa_gain_std_dev_up_risk_maj,
                 oa_gain_std_dev_up_risk_urg, oa_gain_std_dev_low_risk_thr,
                 oa_gain_std_dev_low_risk_maj, oa_gain_std_dev_low_risk_urg,
                 oa_input_power_std_dev_up_risk_thr, oa_input_power_std_dev_up_risk_maj,
                 oa_input_power_std_dev_up_risk_urg, oa_input_power_std_dev_low_risk_thr,
                 oa_input_power_std_dev_low_risk_maj, oa_input_power_std_dev_low_risk_urg,
                 oa_output_power_std_dev_up_risk_thr, oa_output_power_std_dev_up_risk_maj,
                 oa_output_power_std_dev_up_risk_urg, oa_output_power_std_dev_low_risk_thr,
                 oa_output_power_std_dev_low_risk_maj, oa_output_power_std_dev_low_risk_urg,
                 fiber_two_way_dev_risk_thr, fiber_two_way_dev_risk_maj,
                 fiber_two_way_dev_risk_urg, olp_power_dev_risk_thr, olp_power_dev_risk_maj,
                 olp_power_dev_risk_urg, timestamp=datetime.now(), is_history=0):
        self.id = str(uuid.uuid4())
        self.rule_name = rule_name
        self.city = city
        self.net_level = net_level
        self.owner = owner
        self.is_used = is_used
        self.oa_input_power_fluc_risk_thr = oa_input_power_fluc_risk_thr
        self.oa_input_power_fluc_risk_maj = oa_input_power_fluc_risk_maj
        self.oa_input_power_fluc_risk_urg = oa_input_power_fluc_risk_urg
        self.oa_output_power_fluc_risk_thr = oa_output_power_fluc_risk_thr
        self.oa_output_power_fluc_risk_maj = oa_output_power_fluc_risk_maj
        self.oa_output_power_fluc_risk_urg = oa_output_power_fluc_risk_urg
        self.oa_gain_std_dev_up_risk_thr = oa_gain_std_dev_up_risk_thr
        self.oa_gain_std_dev_up_risk_maj = oa_gain_std_dev_up_risk_maj
        self.oa_gain_std_dev_up_risk_urg = oa_gain_std_dev_up_risk_urg
        self.oa_gain_std_dev_low_risk_thr = oa_gain_std_dev_low_risk_thr
        self.oa_gain_std_dev_low_risk_maj = oa_gain_std_dev_low_risk_maj
        self.oa_gain_std_dev_low_risk_urg = oa_gain_std_dev_low_risk_urg
        self.oa_input_power_std_dev_up_risk_thr = oa_input_power_std_dev_up_risk_thr
        self.oa_input_power_std_dev_up_risk_maj = oa_input_power_std_dev_up_risk_maj
        self.oa_input_power_std_dev_up_risk_urg = oa_input_power_std_dev_up_risk_urg
        self.oa_input_power_std_dev_low_risk_thr = oa_input_power_std_dev_low_risk_thr
        self.oa_input_power_std_dev_low_risk_maj = oa_input_power_std_dev_low_risk_maj
        self.oa_input_power_std_dev_low_risk_urg = oa_input_power_std_dev_low_risk_urg
        self.oa_output_power_std_dev_up_risk_thr = oa_output_power_std_dev_up_risk_thr
        self.oa_output_power_std_dev_up_risk_maj = oa_output_power_std_dev_up_risk_maj
        self.oa_output_power_std_dev_up_risk_urg = oa_output_power_std_dev_up_risk_urg
        self.oa_output_power_std_dev_low_risk_thr = oa_output_power_std_dev_low_risk_thr
        self.oa_output_power_std_dev_low_risk_maj = oa_output_power_std_dev_low_risk_maj
        self.oa_output_power_std_dev_low_risk_urg = oa_output_power_std_dev_low_risk_urg
        self.fiber_two_way_dev_risk_thr = fiber_two_way_dev_risk_thr
        self.fiber_two_way_dev_risk_maj = fiber_two_way_dev_risk_maj
        self.fiber_two_way_dev_risk_urg = fiber_two_way_dev_risk_urg
        self.olp_power_dev_risk_thr = olp_power_dev_risk_thr
        self.olp_power_dev_risk_maj = olp_power_dev_risk_maj
        self.olp_power_dev_risk_urg = olp_power_dev_risk_urg
        self.timestamp = timestamp
        self.is_history = is_history

    @classmethod
    def get_input_threshold(cls, **kwargs):
        with Tr_Session() as session:
            query = session.query(cls).filter_by(**kwargs)
            return query.first()

    @classmethod
    def get_threshold_total(cls, history_val, filters):
        with Tr_Session() as session:
            if filters is None:
                return session.query(cls).filter(cls.is_history == history_val).count()
            else:
                query = cls.generate_query(session, history_val, filters)
                return query.count()

    @classmethod
    def get_threshold_by_page_size(cls, history_val, page_idx, page_size, filters):
        idx = 0 if (page_idx - 1) < 0 else page_idx - 1
        start = idx * page_size
        with Tr_Session() as session:
            if filters is None:
                return session.query(cls).filter(cls.is_history == history_val).offset(start).limit(page_size).all()

            query = cls.generate_query(session, history_val, filters)
            return query.offset(start).limit(page_size).all()

    @classmethod
    def get_input_thresholds(cls, **kwargs):
        with Tr_Session() as session:
            return session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def get_specific_threshold(cls, city, rule_name, is_history):
        with Tr_Session() as session:
            query = session.query(cls).filter(cls.city == city)
            query = query.filter(cls.rule_name != rule_name)
            query = query.filter(cls.is_history == is_history)
            return query.first()

    @classmethod
    def update_specific_threshold(cls, city, rule_name, is_history):
        with Tr_Session() as session:
            query = session.query(cls).filter(cls.city == city)
            query = query.filter(cls.rule_name != rule_name)
            query = query.filter(cls.is_history == is_history)
            rows = query.update({cls.is_used: 0})
            return rows > 0

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
    def add_threshold(cls, **kwargs):
        threshold = cls(**kwargs)
        with Tr_Session() as session:
            try:
                session.add(threshold)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
        return threshold

    @classmethod
    def update(cls, rule_name, **kwargs) -> bool:
        with Tr_Session() as session:
            try:
                query = session.query(cls).filter(cls.rule_name == rule_name)
                query = query.filter(cls.is_history == 0)
                updated = query.update(kwargs)
                session.commit()
                return updated > 0
            except Exception as e:
                session.rollback()
                raise e

    @classmethod
    def get_count(cls, **filters) -> int:
        with Tr_Session() as session:
            query = session.query(func.count(inspect(cls).primary_key[0]))
            for key, val in filters.items():
                if isinstance(val, list):
                    query = query.filter(getattr(cls, key).in_(val))
                else:
                    query = query.filter_by(**{key: val})
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
