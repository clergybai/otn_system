from ..models.computing_mode import ComputingMode


def get_computing_state():
    return ComputingMode.get_computed_state()
