from datetime import datetime
from ..models.input_threshold import InputThreshold


def get_default():
    return InputThreshold.get_input_threshold(
        rule_name='default',
        is_history=0)


def get_specific_threshold(city, rule_name, is_history):
    return InputThreshold.get_specific_threshold(
        city=city, rule_name=rule_name, is_history=is_history)


def update_specific_threshold(city, rule_name, is_history):
    return InputThreshold.update_specific_threshold(
        city=city, rule_name=rule_name, is_history=is_history)


def get_outline(page_idx, page_size, filters=None):
    outlines = InputThreshold.get_threshold_by_page_size(0, page_idx, page_size, filters)
    return [{
        "city": line.city,
        "net_level": line.net_level,
        "owner": line.owner,
        "is_used": line.is_used,
        "is_used_bool": True if line.is_used > 0 else False,
        "rule_name": line.rule_name
        } for line in outlines]


def get_threshold_total(filters):
    return InputThreshold.get_threshold_total(0, filters=filters)


def get_input_thread(rule_name, is_history=0):
    return InputThreshold.get_input_threshold(
        rule_name=rule_name, is_history=is_history)


def upsert(**kwargs):
    rule_name = kwargs['rule_name']
    rule = InputThreshold.get_input_threshold(rule_name=rule_name,
                                              is_history=0)
    if rule:
        return InputThreshold.update(rule_name=rule_name, kwargs=kwargs)
    else:
        return InputThreshold.add_threshold(**kwargs)


def delete_threshold(rule_name):
    return InputThreshold.update(
        rule_name=rule_name,
        timestamp=datetime.now(),
        is_history=1)
