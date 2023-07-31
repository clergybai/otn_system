import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.inspection import inspect
from datetime import datetime
from common.database import EmptyModel, tr_session
import uuid


class TopOlp(EmptyModel):
    __tablename__ = "top_olp"

    id = sa.Column(sa.VARCHAR(63), primary_key=True)
    olp_ne_id = sa.Column(sa.VARCHAR(63), default=None)
    olp_shelf_id = sa.Column(sa.VARCHAR(63), default=None)
    olp_slot_id = sa.Column(sa.VARCHAR(63), default=None)
    manual_olp_act_stand_baseline = sa.Column(sa.Double, default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer)

    def __init__(self, olp_ne_id, olp_shelf_id, olp_slot_id,
                 manual_olp_act_stand_baseline, timestamp=datetime.now(), is_history=2):
        self.id = str(uuid.uuid4())
        self.olp_ne_id = olp_ne_id
        self.olp_shelf_id = olp_shelf_id
        self.olp_slot_id = olp_slot_id
        self.manual_olp_act_stand_baseline = manual_olp_act_stand_baseline
        self.timestamp = timestamp
        self.is_history = is_history

    @classmethod
    def all(cls):
        return tr_session.query(cls).all()

    @classmethod
    def get_top_olps(cls, **kwargs):
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
