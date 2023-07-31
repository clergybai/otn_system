import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.inspection import inspect
from datetime import datetime
from common.database import EmptyModel, tr_session
import uuid


class TopGain(EmptyModel):
    __tablename__ = "top_gain"

    id = sa.Column(sa.VARCHAR(63), primary_key=True)
    source_ne_id = sa.Column(sa.VARCHAR(63), default=None)
    source_oa_shelf_id = sa.Column(sa.VARCHAR(63), default=None)
    source_oa_slot_id = sa.Column(sa.VARCHAR(63), default=None)
    manual_gain_baseline = sa.Column(sa.Double, default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer)

    def __init__(self, source_ne_id, source_oa_shelf_id, source_oa_slot_id,
                 manual_gain_baseline, timestamp=datetime.now(), is_history=2):
        self.id = str(uuid.uuid4())
        self.source_ne_id = source_ne_id
        self.source_oa_shelf_id = source_oa_shelf_id
        self.source_oa_slot_id = source_oa_slot_id
        self.manual_gain_baseline = manual_gain_baseline
        self.timestamp = timestamp
        self.is_history = is_history

    @classmethod
    def get(cls, **kwargs):
        return tr_session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def get_top_gains(cls, **kwargs):
        query = tr_session.query(cls).filter_by(**kwargs)
        return query.first()

    @classmethod
    def get_count(cls, **filters) -> int:
        query = tr_session.query(func.count(inspect(cls).primary_key[0]))
        for key, val in filters.items():
            if isinstance(val, list):
                query = query.filter(getattr(cls, key).in_(val))
            else:
                query = query.filter_by(**{key: val})
        count = query.scalar()
        return count

    @classmethod
    def bulk_update(cls, update_mappings):
        tr_session.bulk_update_mappings(cls, update_mappings)
        tr_session.commit()
