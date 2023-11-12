import sqlalchemy as sa
from datetime import datetime
from common.database import EmptyModel, tr_session
import uuid


class FrontDataFiber(EmptyModel):
    __tablename__ = "front_data_fiber"
    
    id = sa.Column(sa.VARCHAR(63), primary_key=True, nullable=False)
    source_ne_id = sa.Column(sa.VARCHAR(63), default=None)
    target_ne_id = sa.Column(sa.VARCHAR(63), nullable=False)
    act_stand = sa.Column(sa.VARCHAR(63), default=None)
    source_sub_name = sa.Column(sa.VARCHAR(63), default=None)
    target_sub_name = sa.Column(sa.VARCHAR(63), default=None)
    fiber_name = sa.Column(sa.Text, default=None)
    fiber_length = sa.Column(sa.Integer, default=None)
    stand_fiber_loss = sa.Column(sa.Double, default=None)
    source_out_fiber_loss = sa.Column(sa.Double, default=None)
    source_in_fiber_loss = sa.Column(sa.Double, default=None)
    source_outing_power = sa.Column(sa.Double, default=None)
    source_out_shelf_slot = sa.Column(sa.VARCHAR(63), default=None)
    source_incoming_power = sa.Column(sa.Double, default=None)
    source_in_shelf_slot = sa.Column(sa.VARCHAR(63), default=None)
    target_outing_power = sa.Column(sa.Double, default=None)
    target_out_shelf_slot = sa.Column(sa.VARCHAR(63), default=None)
    target_incoming_power = sa.Column(sa.Double, default=None)
    target_in_shelf_slot = sa.Column(sa.VARCHAR(63), default=None)
    is_risk = sa.Column(sa.VARCHAR(63), default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer, default=0)
    
    def __init__(self, source_ne_id, target_ne_id, act_stand, source_sub_name, target_sub_name,
                 fiber_name, fiber_length, stand_fiber_loss, source_out_fiber_loss, source_in_fiber_loss,
                 source_outing_power, source_out_shelf_slot, source_incoming_power, source_in_shelf_slot,
                 target_outing_power, target_out_shelf_slot, target_incoming_power, target_in_shelf_slot,
                 is_risk, timestamp=datetime.now(), is_history=2):
        self.id = str(uuid.uuid4())
        self.source_ne_id = source_ne_id
        self.target_ne_id = target_ne_id
        self.act_stand = act_stand
        self.source_sub_name = source_sub_name
        self.target_sub_name = target_sub_name
        self.fiber_name = fiber_name
        self.fiber_length = fiber_length
        self.stand_fiber_loss = stand_fiber_loss
        self.source_out_fiber_loss = source_out_fiber_loss
        self.source_in_fiber_loss = source_in_fiber_loss
        self.source_outing_power = source_outing_power
        self.source_out_shelf_slot = source_out_shelf_slot
        self.source_incoming_power = source_incoming_power
        self.source_in_shelf_slot = source_in_shelf_slot
        self.target_outing_power = target_outing_power
        self.target_out_shelf_slot = target_out_shelf_slot
        self.target_incoming_power = target_incoming_power
        self.target_in_shelf_slot = target_in_shelf_slot
        self.is_risk = is_risk
        self.timestamp = timestamp
        self.is_history = is_history

    @classmethod
    def get(cls, **kwargs):
        return tr_session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def get_from_source_or_target(cls, source, target, **kwargs):
        query = tr_session.query(cls)
        query = query.filter(
            sa.or_(
                sa.and_(cls.source_ne_id == source, cls.target_ne_id == target),
                sa.and_(cls.source_ne_id == target, cls.target_ne_id == source)
            )
        )
        query = query.filter_by(**kwargs)
        return query.first()

    @classmethod
    def bulk_add(cls, kwargs_list):
        calc_ne_oas_list = []
        for kwargs in kwargs_list:
            calc_ne_oas = cls(**kwargs)
            calc_ne_oas_list.append(calc_ne_oas)
        if len(calc_ne_oas_list) > 0:
            tr_session.add_all(calc_ne_oas_list)
            tr_session.commit()
     
