import sqlalchemy as sa
from datetime import datetime
from common.database import EmptyModel, pg_session


class PgInputVoaConfig(EmptyModel):
    __tablename__ = "pg_input_voa_config"

    id = sa.Column(sa.String, primary_key=True, nullable=False)
    sub_name = sa.Column(sa.String)
    ne_id = sa.Column(sa.String)
    shelf_id = sa.Column(sa.String)
    slot_id = sa.Column(sa.String)
    port_id = sa.Column(sa.String)
    voa_vaule = sa.Column(sa.DOUBLE)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer)

    @classmethod
    def get_all(cls):
        return pg_session.query(cls).all()
