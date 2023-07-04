import sqlalchemy as sa
from datetime import datetime
from ..database import EmptyModel, lo_session


class UserPerms(EmptyModel):
    __tablename__ = "user_perms"

    user_name = sa.Column(sa.VARCHAR(31), primary_key=True)
    zone_authen = sa.Column(sa.Text)
    can_add_standrad_param = sa.Column(sa.Integer, default=0)
    can_modify_base_line = sa.Column(sa.Integer, default=0)
    can_threshold_setting = sa.Column(sa.Integer, default=0)
    can_add_user = sa.Column(sa.Integer, default=0)
    can_modify_prems = sa.Column(sa.Integer, default=0)
    can_output_hiddentrouble = sa.Column(sa.Integer, default=0)
    can_save_topo_position = sa.Column(sa.Integer, default=0)
    can_set_channel_num = sa.Column(sa.Integer, default=0)
    create_time = sa.Column(sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP'))
    last_update_person = sa.Column(sa.VARCHAR(31))
    
    def __init__(self, user_name, zone_authen, can_add_standrad_param,
                 can_modify_base_line, can_threshold_setting, can_add_user,
                 can_modify_prems, can_output_hiddentrouble, can_save_topo_position,
                 can_set_channel_num, last_update_person):
        self.user_name = user_name
        self.zone_authen = zone_authen,
        self.can_add_standrad_param= can_add_standrad_param,
        self.can_modify_base_line = can_modify_base_line,
        self.can_threshold_setting = can_threshold_setting,
        self.can_add_user = can_add_user,
        self.can_modify_prems = can_modify_prems,
        self.can_output_hiddentrouble = can_output_hiddentrouble,
        self.can_save_topo_position = can_save_topo_position,
        self.can_set_channel_num = can_set_channel_num,
        self.create_time = datetime.now(),
        self.last_update_person = last_update_person

    def to_dict(self):
        return {
            "user_name": self.user_name,
            "zone_authen": self.zone_authen,
            "can_add_standrad_param": True if self.can_add_standrad_param > 0 else False,
            "can_modify_base_line": True if self.can_modify_base_line > 0 else False,
            "can_threshold_setting": True if self.can_threshold_setting > 0 else False,
            "can_add_user": True if self.can_add_user > 0 else False,
            "can_modify_prems": True if self.can_modify_prems > 0 else False,
            "can_output_hiddentrouble": True if self.can_output_hiddentrouble > 0 else False,
            "can_save_topo_position": True if self.can_save_topo_position > 0 else False,
            "can_set_channel_num": True if self.can_set_channel_num > 0 else False,
            "create_time": self.create_time,
            "last_update_person": self.last_update_person
        }

    @classmethod
    def get_by(cls, **filters):
        return lo_session.query(cls).filter_by(**filters).one_or_none()

    @classmethod
    def get_all_user_perms(cls):
        return lo_session.query(cls).order_by(cls.user_name).all()

    @classmethod
    def add_new_user_perm(cls, **kwargs):
        user_perm = cls(kwargs)
        lo_session.add(user_perm)
        lo_session.commit()
        return user_perm.to_dict()

    @classmethod
    def update(cls, user_name, **kwargs) -> bool:
        updated = lo_session.query(cls).filter_by(user_name=user_name).update(kwargs)
        lo_session.commit()
        return updated > 0
