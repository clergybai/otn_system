from ..models.input_threshold_och import InputThresholdOch


def get_outline(page_idx, page_size, filters=None):
    outlines = InputThresholdOch.get_threshold_och_by_page_size(
        0, page_idx, page_size, filters)
    return [{
        "city": line.city,
        "net_level": line.net_level,
        "owner": line.owner,
        "is_used": line.is_used,
        "is_used_bool": True if line.is_used > 0 else False,
        "rule_name": line.rule_name
    } for line in outlines]


def get_threshold_och_total(filters):
    return InputThresholdOch.get_threshold_och_total(0, filters=filters)
