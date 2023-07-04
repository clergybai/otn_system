import sqlalchemy as sa
from datetime import datetime
from common.database import EmptyModel, pg_session


class PgInputUpdateTimestamp(EmptyModel):
    __tablename__ = "pg_input_update_timestamp"

    pg_input_topology_data = sa.Column(sa.DateTime, nullable=False)
    pg_input_optical_ne = sa.Column(sa.DateTime, nullable=False)
    pg_input_oa_board_type = sa.Column(sa.DateTime, nullable=False)
    pg_input_voa_config = sa.Column(sa.DateTime, nullable=False)
    pg_input_internal_topology = sa.Column(sa.DateTime, nullable=False)
    pg_input_pm_data = sa.Column(sa.DateTime, nullable=False)
    pg_input_voa_back_data = sa.Column(sa.DateTime, nullable=False)

    @classmethod
    def get_all(cls):
        return pg_session.query(cls).all()
