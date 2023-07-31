from sqlalchemy import orm, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sa
import datetime
from urllib.parse import quote_plus as urlquote
from common.config import settings

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{usr}:{pwd}@{db}:{port}/{schema}?charset=utf8mb4".format(
        usr=settings.db_lo_username,
        pwd=urlquote(settings.db_lo_password),
        db=settings.db_lo_hostname,
        port=settings.db_lo_port,
        schema=settings.db_lo_schema
    )

DB_TRANS_SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{usr}:{pwd}@{db}:{port}/{schema}?charset=utf8mb4".format(
        usr=settings.db_tr_username,
        pwd=urlquote(settings.db_tr_password),
        db=settings.db_tr_hostname,
        port=settings.db_tr_port,
        schema=settings.db_tr_schema
    )

engine = create_engine(SQLALCHEMY_DATABASE_URL)
db_transnet_engine = create_engine(DB_TRANS_SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
DB_Transnet_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_transnet_engine)

session = orm.scoped_session(SessionLocal)
db_trnas_session = orm.scoped_session(DB_Transnet_SessionLocal)

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
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
