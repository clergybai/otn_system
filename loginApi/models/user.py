import sqlalchemy as sa
from sqlalchemy import func
import datetime
from ..database import EmptyModel, lo_session


class User(EmptyModel):
    __tablename__ = "user"

    user_name = sa.Column(sa.VARCHAR(31), primary_key=True)
    name = sa.Column(sa.VARCHAR(15), nullable=False)
    salt = sa.Column(sa.VARCHAR(63), nullable=True)
    user_email = sa.Column(sa.VARCHAR(63), nullable=False)
    cellphone_num = sa.Column(sa.VARCHAR(31), nullable=False)
    city = sa.Column(sa.VARCHAR(15), default=None)
    role = sa.Column(sa.Integer)
    department = sa.Column(sa.VARCHAR(15), default=None)
    post = sa.Column(sa.VARCHAR(15), default=None)
    remark = sa.Column(sa.VARCHAR(255), default=None)
    is_active = sa.Column(sa.Integer, default=1)
    create_time = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    update_time = sa.Column(sa.DateTime, default=datetime.datetime.utcnow,
                            onupdate=datetime.datetime.utcnow)
    last_update_person = sa.Column(sa.VARCHAR(31), nullable=False)

    def __repr__(self) -> str:
        return '<User {usrname}>'.format(usrname=self.user_name)

    def __init__(self, user_name, name, salt, user_email, cellphone_num, city,
                 role, department, post, remark, is_active, last_update_person):
        self.user_name = user_name
        self.name = name
        self.salt = salt
        self.user_email = user_email
        self.cellphone_num = cellphone_num
        self.city = city
        self.role = role
        self.department = department
        self.post = post
        self.remark = remark
        self.is_active = is_active
        self.last_update_person = last_update_person

    def to_dict(self):
        return {
            "user_name": self.user_name,
            "name": self.name,
            "salt": None,
            "user_email": self.user_email,
            "cellphone_num": self.cellphone_num,
            "city": self.city,
            "role": self.role,
            "department": self.department,
            "post": self.post,
            "remark": self.remark,
            "is_active": self.is_active,
            "create_time": self.create_time,
            "update_time": self.update_time,
            "last_update_person": self.last_update_person
        }

    @classmethod
    def find_user_by(cls, **kwargs):
        return lo_session.query(cls).filter_by(**kwargs).one_or_none()

    @classmethod
    def get_users_num(cls):
        return lo_session.query(func.count(cls.user_name).label('count')).scalar()

    @classmethod
    def get_users(cls, **kwargs):
        query = lo_session.query(cls)
        for key, val in kwargs.items():
            query = query.filter(getattr(cls, key).like('%'+val+'%'))
        return query.order_by(cls.user_name).all()

    @classmethod
    def add_user(cls, **kwargs):
        new_user = cls(
            **kwargs)
        lo_session.add(new_user)
        lo_session.commit()

    @classmethod
    def update_user(cls, user_name, **kwargs):
        rows_updated = lo_session.query(cls).filter_by(user_name=user_name).update(kwargs)
        lo_session.commit()
        if rows_updated > 0:
            return True
        return False
