import sqlalchemy as sa
from common.database import EmptyModel, tr_session


class InputUpdateTimestamp(EmptyModel):
    __tablename__ = "input_update_timestamp"

    id = sa.Column(sa.INTEGER, primary_key=True)
    input_topology_data = sa.Column(sa.DateTime, nullable=False)
    input_optical_ne = sa.Column(sa.DateTime, nullable=False)
    input_oa_board_type = sa.Column(sa.DateTime, nullable=False)
    input_voa_config = sa.Column(sa.DateTime, nullable=False)
    input_internal_topology = sa.Column(sa.DateTime, nullable=False)
    input_pm_data = sa.Column(sa.DateTime, nullable=False)
    input_voa_back_data = sa.Column(sa.DateTime, nullable=False)

    @classmethod
    def get_all(cls):
        return tr_session.query(cls).all()
