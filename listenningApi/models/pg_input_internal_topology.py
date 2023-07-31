import sqlalchemy as sa
from common.database import EmptyModel, pg_session


class PgInputInternalTopology(EmptyModel):
    __tablename__ = "pg_input_internal_topology"

    id = sa.Column(sa.String, primary_key=True, nullable=False)
    a_sub_name = sa.Column(sa.String)
    a_ne_id = sa.Column(sa.String)
    a_shelf_id = sa.Column(sa.String)
    a_slot_id = sa.Column(sa.String)
    a_port_id = sa.Column(sa.String)
    a_in_out_id = sa.Column(sa.String)
    a_board_model = sa.Column(sa.String)
    z_sub_name = sa.Column(sa.String)
    z_ne_id = sa.Column(sa.String)
    z_shelf_id = sa.Column(sa.String)
    z_slot_id = sa.Column(sa.String)
    z_port_id = sa.Column(sa.String)
    z_in_out_id = sa.Column(sa.String)
    z_board_model = sa.Column(sa.String)

    @classmethod
    def get_all(cls):
        return pg_session.query(cls).all()