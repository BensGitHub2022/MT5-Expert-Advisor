from src.shared_helper_functions import calc_lot_size


def test_calc_lot_size():
    assert calc_lot_size(0.1, 50) == 10