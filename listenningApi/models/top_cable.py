import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.inspection import inspect
from datetime import datetime
from common.database import EmptyModel, tr_session
import uuid


class TopCable(EmptyModel):
    __tablename__ = "top_cable"

    id = sa.Column(sa.VARCHAR(63), primary_key=True)
    source_ne_id = sa.Column(sa.VARCHAR(63), default=None)
    target_ne_id = sa.Column(sa.VARCHAR(63), default=None)
    act_stand = sa.Column(sa.VARCHAR(63), default=None)
    manual_cable_in_out_baseline = sa.Column(sa.Double, default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer)

    def __init__(self, source_ne_id, target_ne_id, act_stand,
                 manual_cable_in_out_baseline, timestamp=datetime.now(), is_history=2):
        self.id = str(uuid.uuid4())
        self.source_ne_id = source_ne_id
        self.target_ne_id = target_ne_id
        self.act_stand = act_stand
        self.manual_cable_in_out_baseline = manual_cable_in_out_baseline
        self.timestamp = timestamp
        self.is_history = is_history

    @classmethod
    def get_top_cables(cls, **kwargs):
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
