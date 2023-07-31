import sqlalchemy as sa
from datetime import datetime
from common.database import EmptyModel, pg_session


class PgInputOpticalNe(EmptyModel):
    __tablename__ = "pg_input_optical_ne"

    ne_id = sa.Column(sa.String, primary_key=True, nullable=False)
    ne_name = sa.Column(sa.String)
    city = sa.Column(sa.String)
    district_county = sa.Column(sa.String)
    manufactor = sa.Column(sa.String)
    network_level = sa.Column(sa.String)
    ne_type = sa.Column(sa.String)
    ne_model = sa.Column(sa.String)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer)

    @classmethod
    def get_all(cls):
        return pg_session.query(cls).all()
