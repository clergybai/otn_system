import sqlalchemy as sa
from datetime import datetime
from common.database import EmptyModel, tr_session
import uuid

class RiskOa(EmptyModel):
    __tablename__ = "risk_oa"
    
    id = sa.Column(sa.VARCHAR(63), primary_key=True, nullable=False)
    city = sa.Column(sa.VARCHAR(63), default=None)
    net_level = sa.Column(sa.VARCHAR(63), default=None)
    source_ne_id = sa.Column(sa.VARCHAR(63), default=None)
    source_oa_shelf_id = sa.Column(sa.VARCHAR(63), default=None)
    source_oa_slot_id = sa.Column(sa.VARCHAR(63), default=None)
    oa_input_power_fluc_risk = sa.Column(sa.Double, default=None)
    optical_power_baseline = sa.Column(sa.Double, default=None)
    is_input_power_fluc_risk = sa.Column(sa.VARCHAR(63), nullable=False, default='0')
    is_input_power_fluc_emergency = sa.Column(sa.VARCHAR(63), nullable=False, default='0')
    oa_output_power_fluc_risk = sa.Column(sa.Double, default=None)
    is_output_power_fluc_risk = sa.Column(sa.VARCHAR(63), nullable=False, default='0')
    is_output_power_fluc_emergency = sa.Column(sa.VARCHAR(63), nullable=False, default='0')
    oa_gain_std_dev_risk = sa.Column(sa.Double, default=None)
    gain_baseline = sa.Column(sa.Double, default=None)
    is_gain_risk = sa.Column(sa.VARCHAR(63), default=None)
    is_gain_emergency = sa.Column(sa.VARCHAR(63), default=None)
    oa_output_power_std_dev_risk = sa.Column(sa.Double, default=None)
    standard_wave_output = sa.Column(sa.Double, default=None)
    is_output_power_dev_risk = sa.Column(sa.VARCHAR(63), default=None)
    is_output_power_dev_emergency = sa.Column(sa.VARCHAR(63), default=None)
    sum_risks = sa.Column(sa.Integer, default=None)
    timestamp = sa.Column(sa.DateTime, nullable=False, default=datetime.now())
    is_history = sa.Column(sa.Integer, default=0)
    
    def __init__(self, city, net_level, source_ne_id, source_oa_shelf_id, source_oa_slot_id,
                 oa_input_power_fluc_risk, optical_power_baseline, is_input_power_fluc_risk,
                 is_input_power_fluc_emergency, oa_output_power_fluc_risk, is_output_power_fluc_risk,
                 is_output_power_fluc_emergency, oa_gain_std_dev_risk, gain_baseline, is_gain_risk,
                 is_gain_emergency, oa_output_power_std_dev_risk, standard_wave_output, is_output_power_dev_risk,
                 is_output_power_dev_emergency, sum_risks, timestamp=datetime.now(), is_history=2):
        self.id = str(uuid.uuid4())
        self.city = city
        self.net_level = net_level
        self.source_ne_id = source_ne_id
        self.source_oa_shelf_id = source_oa_shelf_id
        self.source_oa_slot_id = source_oa_slot_id
        self.oa_input_power_fluc_risk = oa_input_power_fluc_risk
        self.optical_power_baseline = optical_power_baseline
        self.is_input_power_fluc_risk = is_input_power_fluc_risk
        self.is_input_power_fluc_emergency = is_input_power_fluc_emergency
        self.oa_output_power_fluc_risk = oa_output_power_fluc_risk
        self.is_output_power_fluc_risk = is_output_power_fluc_risk
        self.is_output_power_fluc_emergency = is_output_power_fluc_emergency
        self.oa_gain_std_dev_risk = oa_gain_std_dev_risk
        self.gain_baseline = gain_baseline
        self.is_gain_risk = is_gain_risk
        self.is_gain_emergency = is_gain_emergency
        self.oa_output_power_std_dev_risk = oa_output_power_std_dev_risk
        self.standard_wave_output = standard_wave_output
        self.is_output_power_dev_risk = is_output_power_dev_risk
        self.is_output_power_dev_emergency = is_output_power_dev_emergency
        self.sum_risks = sum_risks
        self.timestamp = timestamp,
        self.is_history = is_history
        
    @classmethod
    def get(cls, **kwargs):
        return tr_session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def bulk_add(cls, kwargs_list):
        calc_ne_oas_list = []
        for kwargs in kwargs_list:
            calc_ne_oas = cls(**kwargs)
            calc_ne_oas_list.append(calc_ne_oas)
        if len(calc_ne_oas_list) > 0:
            tr_session.add_all(calc_ne_oas_list)
            tr_session.commit()
        
