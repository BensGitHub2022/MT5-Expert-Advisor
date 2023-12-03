
import pytest
from src.meta_trader_mock import MetaTraderMock
from src.interfaces import Trade

def test_meta_trader():
    meta = MetaTraderMock()
    t = Trade()
    assert meta.execute_trade(t) == "Traded!"

