from .database import Base, EmptyModel, session, Model

from sqlalchemy.sql.expression import text
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, func
import sqlalchemy as sa
from werkzeug import security
from datetime import datetime
from .fileds import CommaList
from functools import reduce
import json


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(String(255), nullable=False)
    published = Column(Boolean, default=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,  server_default=text('now()'))


# Role related model
class User(EmptyModel):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    user_name = sa.Column(sa.Unicode(31), primary_key=True)
    name = sa.Column(sa.Unicode(128), index=True, unique=True)
    salt = sa.Column(sa.Unicode(128))
    user_email = sa.Column(sa.Unicode(63), nullable=False)
    cellphone_num = sa.Column(sa.Unicode(31), nullable=False)
    city = sa.Column(sa.Unicode(15))
    # roles = sa.Column(CommaList(1023), default=(), nullable=False)
    department = sa.Column(sa.Unicode(15))
    post = sa.Column(sa.VARCHAR(15))
    remark = sa.Column(sa.VARCHAR(255))
    is_active = sa.Column(sa.Integer)
    create_time = sa.Column(sa.DateTime, default=datetime.utcnow)
    update_time = sa.Column(sa.DateTime, default=datetime.utcnow,
                            onupdate=datetime.utcnow)
    # the roles allowed to the user
    # wec_userid = sa.Column(sa.String(128), unique=True)
    last_update_person = sa.Column(sa.Unicode(31), nullable=False)
    roles = sa.Column(CommaList(1023), default=(), nullable=False)

    @property
    def permissions(self):
        return Role.aggregate_permissions(self.roles)

    @property
    def zone_authens(self):
        return UserPerms.get_user_zone_authen(self.user_name)

    def __init__(self, user_name, name, salt, user_email, cellphone_num, city,
                 department, post, remark, is_active, last_update_person, roles=None,
                 ):
        self.user_name = user_name
        self.name = name
        self.set_password(salt)
        self.user_email = user_email
        self.cellphone_num = cellphone_num
        self.city = city
        self.roles = roles
        self.department = department
        self.post = post
        self.remark = remark
        self.is_active = is_active
        self.last_update_person = last_update_person
        # self.wec_userid = wec_userid

    def __repr__(self) -> str:
        return '<User %r>' % self.user_name

    @staticmethod
    def _hash_password(raw):
        return security.generate_password_hash(raw)

    def set_password(self, raw):
        self.salt = self._hash_password(raw)

    def check_password(self, raw):
        return security.check_password_hash(self.salt, raw)

    @classmethod
    def find_user_by(cls, **kwargs):
        return session.query(cls).filter_by(**kwargs).one_or_none()

    @classmethod
    def get_users(cls, start, stop):
        return session.query(cls).slice(start, stop).all()

    @classmethod
    def get_users_num(cls):
        return session.query(func.count(cls.name).label('count')).scalar()

    @classmethod
    def check_duplicate(cls, **kwargs):
        for key in kwargs:
            if kwargs[key] is not None and cls.find_user_by(**{key: kwargs[key]}) is not None:
                return key, f'{key}: {kwargs[key]} is already exists.'

        return None, 'nodup'

    @classmethod
    def check_duplicate_with_others(cls, name_, **kwargs):
        for key in kwargs:
            if kwargs[key] is not None and session.query(cls).filter(cls.name != name_).filter_by(
                    **{key: kwargs[key]}).one_or_none() is not None:
                return key, f'{key}: {kwargs[key]} is already exists.'

        return None, 'nodup'

    @classmethod
    def add_user(cls, user):
        session.add(user)
        session.commit()
        return user.id

    @classmethod
    def update_user(cls, name_, update_fields):
        session.query(cls).filter(cls.name == name_).update(update_fields,
                                                            synchronize_session=False)
        session.commit()

    @classmethod
    def update_password(cls, name_, raw_password):
        session.query(cls).filter(cls.name == name_).update(
            {"password": cls._hash_password(raw_password)}, synchronize_session=False)
        session.commit()


class SysProp(Model):
    __tablename__ = 'sys_props'
    __table_args__ = {'extend_existing': True}

    name = sa.Column(sa.String(64), nullable=False, unique=True)
    content = sa.Column(sa.Unicode(255))

    @classmethod
    def get(cls, name):
        value = session.query(cls.content).filter(cls.name == name).one_or_none()
        return value[0] if value else None


class Permission(Model):
    __tablename__ = 'permissions'
    __table_args__ = {'extend_existing': True}

    name = sa.Column(sa.String(128), nullable=False, unique=True)
    description = sa.Column(sa.Unicode(255))

    # Define all the permissions, no any reference
    permissions = [
        'console:user',
        'console:config',
        'msgrepo:browse',
        'msgrepo:contact_management'
        'msgrepo:review:ae',
        'msgrepo:review:compliance',
        'lepus:rule:ae',
        'lepus:rule:compliance',
        'lepus:rule:effectiveness',
        'lepus:review:effectiveness'
    ]


class Role(Model):
    __tablename__ = 'roles'
    __table_args__ = {'extend_existing': True}

    name = sa.Column(sa.String(128), nullable=False, unique=True)
    label = sa.Column(sa.Unicode(128))
    description = sa.Column(sa.Unicode(255))
    permissions = sa.Column(CommaList(2047), default=())

    @classmethod
    def get_roles(cls):
        return session.query(cls).all()

    @classmethod
    def aggregate_permissions(cls, roles):
        query = session.query(cls.permissions).filter(cls.name.in_(roles))
        return list(reduce(lambda x, y: x | y, (set(role_perms) for role_perms, in query.all())))


class UserPerms(EmptyModel):
    __tablename__ = 'user_perms'
    __table_args__ = {'extend_existing': True}

    user_name = sa.Column(sa.Unicode(31), primary_key=True)
    zone_authen = sa.Column(sa.TEXT(16777216))
    create_time = sa.Column(sa.DateTime, default=datetime.utcnow)
    last_update_person = sa.Column(sa.VARCHAR(31), nullable=False)

    @classmethod
    def get_user_zone_authen(cls, usr_name):
        zone_authen = session.query(cls.zone_authen).filter_by(user_name=usr_name).one_or_none()
        return None if zone_authen is None else json.loads(zone_authen[0])

