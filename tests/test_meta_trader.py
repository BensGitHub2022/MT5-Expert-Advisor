
import pytest
from src.context_sim import ContextSimulator
from src.interfaces import Trade

def test_meta_trader():
    meta = ContextSimulator()
    t = Trade()
    assert meta.execute_trade(t) == "Traded!"

