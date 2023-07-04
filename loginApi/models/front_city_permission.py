import sqlalchemy as sa
from ..database import EmptyModel, lo_session

import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


class FrontCityPermission(EmptyModel):
    __tablename__ = "front_city_permission"

    id = sa.Column(sa.VARCHAR(63), primary_key=True)
    net_level = sa.Column(sa.VARCHAR(255))
    city = sa.Column(sa.VARCHAR(255))
    sys_name = sa.Column(sa.VARCHAR(255))
    is_history = sa.Column(sa.Integer)

    @classmethod
    def get_by_one(cls, **filters):
        return lo_session.query(cls).filter_by(**filters).one_or_none()

    @classmethod
    def get_by(cls, distinct_field, field_list, **filters):
        query_attrs = [getattr(cls, field_name) for field_name in field_list]
        distinct_attr = getattr(cls, distinct_field)
        query = lo_session.query(*query_attrs)

        for key, val in filters.items():
            if isinstance(val, list):
                query = query.filter(getattr(cls, key).in_(val))
            else:
                query = query.filter_by(**{key: val})
        query = query.distinct(distinct_attr)
        return query.all()

    @classmethod
    def get_cities(cls):
        return lo_session.query(cls.city).filter(cls.net_level.like('本地%')).group_by(cls.city).all()
