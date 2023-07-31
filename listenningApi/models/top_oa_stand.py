import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.inspection import inspect
from datetime import datetime
from common.database import EmptyModel, tr_session
import uuid


class TopOaStand(EmptyModel):
    __tablename__ = "top_oa_stand"

    id = sa.Column(sa.VARCHAR(63), primary_key=True)
    oa_fingerprint = sa.Column(sa.VARCHAR(127), nullable=False)
    manual_standard_wave_output = sa.Column(sa.Double, default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer)

    def __init__(self, oa_fingerprint, manual_standard_wave_output,
                 timestamp=datetime.now(), is_history=2):
        self.id = str(uuid.uuid4())
        self.oa_fingerprint = oa_fingerprint
        self.manual_standard_wave_output = manual_standard_wave_output
        self.timestamp = timestamp
        self.is_history = is_history

    @classmethod
    def get(cls, **kwargs):
        return tr_session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def get_top_oa_stands(cls, **kwargs):
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
