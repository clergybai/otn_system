import sqlalchemy as sa
import uuid
from datetime import datetime
from common.database import EmptyModel, tr_session


class InputVoaConfig(EmptyModel):
    __tablename__ = "input_voa_config"

    id = sa.Column(sa.VARCHAR(63), primary_key=True)
    sub_name = sa.Column(sa.VARCHAR(255), default=None)
    ne_id = sa.Column(sa.VARCHAR(63), default=None)
    shelf_id = sa.Column(sa.VARCHAR(63), default=None)
    slot_id = sa.Column(sa.VARCHAR(63), default=None)
    port_id = sa.Column(sa.VARCHAR(63), default=None)
    voa_vaule = sa.Column(sa.Float, default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer)

    def __init__(self, sub_name, ne_id, shelf_id, slot_id, port_id,
                 voa_vaule, timestamp, is_history):
        self.id = str(uuid.uuid4())
        self.sub_name = sub_name
        self.ne_id = ne_id
        self.shelf_id = shelf_id
        self.slot_id = slot_id
        self.port_id = port_id
        self.voa_vaule = voa_vaule
        self.timestamp = timestamp
        self.is_history = is_history

    @classmethod
    def get_input_voa_configs(cls, **kwargs):
        return tr_session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def get_voa_configs_by_page_size(cls, history_val, page_idx, page_size, filters):
        idx = 0 if (page_idx - 1) < 0 else page_idx - 1
        start = idx * page_size
        if filters is None:
            return tr_session.query(cls).filter(cls.is_history > history_val).offset(start).limit(page_size).all()

        query = cls.generate_query(history_val, filters)
        return query.offset(start).limit(page_size).all()

    @classmethod
    def get_voa_configs_total(cls, history_val, filters):
        if filters is None:
            return tr_session.query(cls).filter(cls.is_history > history_val).count()
        else:
            query = cls.generate_query(history_val, filters)
            return query.count()

    @classmethod
    def generate_query(cls, history_val, filters):
        query = tr_session.query(cls).filter(cls.is_history > history_val)
        for filter in filters:
            if len(filter.items()):
                field_name = filter['name']
                values = filter['values']
                if isinstance(values, list):
                    query = query.filter(getattr(cls, field_name).in_(values))
                else:
                    query = query.filter_by(**{field_name: values})
        return query

    @classmethod
    def bulk_add(cls, kwargs_list):
        input_voa_config_list = []
        for kwargs in kwargs_list:
            input_top_data = cls(**kwargs)
            input_voa_config_list.append(input_top_data)
        if len(input_voa_config_list) > 0:
            tr_session.add_all(input_voa_config_list)
            tr_session.commit()

    @classmethod
    def update(cls, filters, **kwargs):
        return tr_session.query(cls).filter_by(**filters).update(**kwargs)
