
import pytest
from src.context_factory import MetaTraderFactory
from src.context_mt5 import ContextMT5
from src.context_sim import ContextSimulator


def test_meta_trader_factory_create_production():
    factory = MetaTraderFactory(True)
    meta = factory.create_meta_trader()
    assert type(meta) == ContextMT5

def test_meta_trader_factory_create_mock():
    factory = MetaTraderFactory(False)
    meta = factory.create_meta_trader()
    assert type(meta) == ContextSimulator
