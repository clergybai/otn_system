import sqlalchemy as sa
from datetime import datetime
from common.database import EmptyModel, tr_session


class ObjNode(EmptyModel):
    __tablename__ = "obj_node"

    id = sa.Column(sa.VARCHAR(63), primary_key=True, nullable=False)
    sys_id = sa.Column(sa.VARCHAR(63), nullable=False)
    ne_name = sa.Column(sa.VARCHAR(63), default=None)
    ne_sub_name = sa.Column(sa.VARCHAR(63), default=None)
