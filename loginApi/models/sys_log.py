import sqlalchemy as sa
from datetime import datetime
from common.database import EmptyModel, Lo_Session


class SysLog(EmptyModel):
    __tablename__ = "sys_log"

    id = sa.Column(sa.VARCHAR(63), primary_key=True)
    op_module = sa.Column(sa.VARCHAR(250), nullable=False)
    op_user = sa.Column(sa.VARCHAR(250), nullable=False)
    op_behavior = sa.Column(sa.VARCHAR(250), nullable=False)
    op_time = sa.Column(sa.DateTime(), default=datetime.now())

    def __init__(self, id, op_module, op_user, op_behavior):
        self.id = id
        self.op_module = op_module
        self.op_user = op_user
        self.op_behavior = op_behavior

    def __repr__(self) -> str:
        return f"id: {self.id}, {self.op_module}"

    def to_dict(self):
        return {
            "id": self.id,
            "op_module": self.op_module,
            "op_user": self.op_user,
            "op_behavior": self.op_behavior,
            "op_time": self.op_time.strftime("%m/%d/%Y %H:%M:%S")
        }

    @classmethod
    def add_log(cls, log):
        with Lo_Session() as session:
            try:
                session.add(log)
                session.commit()
            except Exception as e:
                session.rollback(e)
                raise e
            return log.id

    @classmethod
    def get_log(cls, **kwargs):
        with Lo_Session() as session:
            query = session.query(cls)
            for key, val in kwargs.items():
                if key == "startTime":
                    query = query.filter(cls.op_time >= val)
                if key == "endTime":
                    query = query.filter(cls.op_time < val)
                if key == "op_user":
                    query = query.filter(cls.op_user.like('%'+val+'%'))
            return query.order_by(sa.desc(cls.op_time)).all()
