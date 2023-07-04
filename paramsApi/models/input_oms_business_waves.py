import sqlalchemy as sa
import uuid
from datetime import datetime
from common.database import EmptyModel, tr_session


class InputOmsBusinessWaves(EmptyModel):
    __tablename__ = "input_oms_business_waves"

    id = sa.Column(sa.VARCHAR(63), primary_key=True)
    sys_name = sa.Column(sa.VARCHAR(63), default=None)
    net_level = sa.Column(sa.VARCHAR(63), default=None)
    city = sa.Column(sa.VARCHAR(63), default=None)
    a_sub_name = sa.Column(sa.VARCHAR(255), default=None)
    a_ne_id = sa.Column(sa.VARCHAR(63), default=None)
    z_sub_name = sa.Column(sa.VARCHAR(255), default=None)
    z_ne_id = sa.Column(sa.VARCHAR(63), default=None)
    business_waves = sa.Column(sa.INTEGER, default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer)

    def __init__(self, sys_name, net_level, city, a_sub_name,
                 a_ne_id, z_sub_name, z_ne_id, business_waves,
                 timestamp=datetime.now(), is_history=0):
        self.id = str(uuid.uuid4())
        self.sys_name = sys_name
        self.net_level = net_level
        self.city = city
        self.a_sub_name = a_sub_name
        self.a_ne_id = a_ne_id
        self.z_sub_name = z_sub_name
        self.z_ne_id = z_ne_id
        self.business_waves = business_waves
        self.timestamp = timestamp
        self.is_history = is_history

    @classmethod
    def get_oms_by_filter(cls, **kwargs):
        param = kwargs.get('param')
        city_list = []
        filter_city_list = False
        if param:
            selected = param.get('selected')
            if selected:
                city_list = selected

        query = tr_session.query(cls)
        # handle filter
        filters = kwargs.get("filter")
        if filters:
            for item in filters:
                if len(item.items()) > 0:
                    name = item.get('name')
                    if name == 'city':
                        filter_city_list = True
                        city_list = item.get('values')
                    elif name:
                        query.filter(getattr(cls, name).in_(item.get('values')))

        if filter_city_list:
            query = query.filter(getattr(cls, 'city').in_(city_list))
        page_idx = kwargs.get('page_index_begin')
        page_size = kwargs.get('page_size')
        total = query.count()
        query = query.order_by(cls.sys_name)

        if page_idx is not None and page_size is not None:
            idx = 0 if (page_idx - 1) < 0 else page_idx - 1
            start = idx * page_size
            query = query.offset(start).limit(page_size)
        return (total, query.all())
