from sqlalchemy import orm, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sa
import datetime
from urllib.parse import quote_plus as urlquote
from common.config import settings


LO_SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{usr}:{pwd}@{db}:{port}/{schema}?charset=utf8mb4".format(
        usr=settings.db_lo_username,
        pwd=urlquote(settings.db_lo_password),
        db=settings.db_lo_hostname,
        port=settings.db_lo_port,
        schema=settings.db_lo_schema
    )

TR_SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{usr}:{pwd}@{db}:{port}/{schema}?charset=utf8mb4".format(
        usr=settings.db_lo_username,
        pwd=urlquote(settings.db_tr_password),
        db=settings.db_tr_hostname,
        port=settings.db_tr_port,
        schema=settings.db_tr_schema
    )

lo_engine = create_engine(LO_SQLALCHEMY_DATABASE_URL)
tr_engine = create_engine(TR_SQLALCHEMY_DATABASE_URL)

Lo_Session = sessionmaker(autocommit=False, autoflush=False, bind=lo_engine)
Tr_Session = sessionmaker(autocommit=False, autoflush=False, bind=tr_engine)
lo_session = orm.scoped_session(Lo_Session)
tr_session = orm.scoped_session(Tr_Session)


Base = declarative_base()


class ModelBase(object):

    id = sa.Column(sa.Integer, primary_key=True)

    created_on = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    modified_on = sa.Column(sa.DateTime, default=datetime.datetime.utcnow,
                            onupdate=datetime.datetime.utcnow)

    def __repr__(self):
        name = type(self).__name__
        return f'<{name}: {self.id}>'


class EmptyModelBase(object):

    def __repr__(self):
        name = type(self).__name__
        return f'<{name}>'


Model = declarative_base(cls=ModelBase)
EmptyModel = declarative_base(cls=EmptyModelBase)

# Dependency
def get_api_db():
    db = Lo_Session()
    try:
        yield db
    finally:
        db.close()